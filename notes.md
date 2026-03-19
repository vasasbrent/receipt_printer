From the proxyfix addition (note on nginx config):

ProxyFix is part of werkzeug, which Flask already depends on — no new packages to install.

  A few things worth knowing:
  - Local dev is unaffected. When you run python site/back/backend.py directly (no proxy), there's no X-Forwarded-For header, so ProxyFix just passes remote_addr through unchanged. Rate limiting works fine locally.
  - If you stack two proxies (e.g., Cloudflare in front of nginx in front of Flask), you'd set x_for=2. One proxy = x_for=1.
  - Your reverse proxy must actually set the header. In nginx this is proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; in your server block 
    - most standard configs include this already.
