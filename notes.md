From the proxyfix addition (note on nginx config):

ProxyFix is part of werkzeug, which Flask already depends on — no new packages to install.

  A few things worth knowing:
  - Local dev is unaffected. When you run python site/back/backend.py directly (no proxy), there's no X-Forwarded-For header, so ProxyFix just passes remote_addr through unchanged. Rate limiting works fine locally.
  - If you stack two proxies (e.g., Cloudflare in front of nginx in front of Flask), you'd set x_for=2. One proxy = x_for=1.
  - Your reverse proxy must actually set the header. In nginx this is proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; in your server block 
    - most standard configs include this already.

  
## 2026-03-21
  
  * Check in on placeholder in index.html line 38
  * Default poet might be borked in script.js line 12, nvm all good

  
uv run --with gunicorn --with flask --with flask_limiter gunicorn --chdir site/back -w 4 -b 0.0.0.0:8000 'backend:receipt_backend_app'

## For systemd .service setup

  Setup steps:

  1. Create system user (on the server):
  sudo useradd -r -m -d /var/lib/receipt-printer -s /usr/sbin/nologin receipt-printer

  2. Copy systemd files to /etc/systemd/system/:
  sudo cp scripts/receipt-printer.socket /etc/systemd/system/
  sudo cp scripts/receipt-printer.service /etc/systemd/system/

  3. Update paths in the service file — replace /opt/receipt-printer with your actual deployment path:
  sudo nano /etc/systemd/system/receipt-printer.service
  # Change WorkingDirectory=/opt/receipt-printer to your path

  4. Reload systemd and enable the service:
  sudo systemctl daemon-reload
  sudo systemctl enable receipt-printer.socket receipt-printer.service
  sudo systemctl start receipt-printer.socket receipt-printer.service

  5. Configure nginx to proxy to the Unix socket. Add to your nginx config:
  upstream gunicorn {
      server unix:/run/receipt-printer.sock fail_timeout=0;
  }

  server {
      listen 80;
      server_name _;

      location / {
          proxy_pass http://gunicorn;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }

  6. Manage the service:
  sudo systemctl status receipt-printer
  sudo systemctl restart receipt-printer
  sudo journalctl -u receipt-printer -f  # tail logs

  The socket activation setup means the service only runs when needed, and logs go to systemd journal.

### Error Message

Second one, there was also an issue with the way uv was begin called.

```console
Mar 22 06:57:33 debian-server (uv)[2559977]: receipt-printer.service: Failed to set up mount namespacing: /run/systemd/unit-root/opt/receipt-printer: No such fi>
```

We need to:
1. Set up nginx to reverse proxy print requests to the gunicorn instance
2. Reconfigure gunicorn so that it actually launches
  1. Current error: `(uv)[2562067]: receipt-printer.service: Failed to set up mount namespacing: /run/systemd/unit-root/opt/receipt-printer: No such file or directory.`

For item 1:
```
server {
    listen 80;
    server_name your-domain.com;

    # Serve static frontend files
    location / {
        alias /path/to/site/front/;
        try_files $uri $uri/ /index.html;  # Serve index.html for SPA routing
    }

    # Proxy API requests to the backend
    location /print {
        proxy_pass http://127.0.0.1:8000;  # or wherever Gunicorn is running
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Several Issues Later

```
⏺ ProtectSystem=strict makes the entire filesystem read-only, including /run, so gunicorn can't use the socket there.

  The proper systemd fix is RuntimeDirectory, which creates a writable directory under /run/ for the service within the protected namespace. You'll need to update both files:

  receipt-printer.service — add to [Service]:
  RuntimeDirectory=receipt-printer
  RuntimeDirectoryMode=0755
  And update the bind path:
  --bind=unix:/run/receipt-printer/gunicorn.sock \

  receipt-printer.socket — update the listen path:
  ListenStream=/run/receipt-printer/gunicorn.sock

  And update your nginx proxy_pass to match:
  proxy_pass http://unix:/run/receipt-printer/gunicorn.sock;

  RuntimeDirectory is the right tool here — it handles creation, ownership, and cleanup of the /run subdirectory automatically as part of the service lifecycle.
```
