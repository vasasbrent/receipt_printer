import os
import subprocess

from flask import Flask, jsonify, request, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "front")

receipt_backend_app = Flask(__name__)

# Tell Flask to trust exactly one proxy hop (your reverse proxy, e.g. nginx/Caddy).
# This makes request.remote_addr reflect the real visitor IP from X-Forwarded-For,
# while ignoring any X-Forwarded-For header a malicious client might send directly.
# x_for=1 means "there is 1 trusted proxy between Flask and the internet".
# If you're NOT behind a reverse proxy, remove this line — it's only needed in production.
receipt_backend_app.wsgi_app = ProxyFix(receipt_backend_app.wsgi_app, x_for=1)

# Configure Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=receipt_backend_app,
    default_limits=["10 per minute"],  # global fallback
)


@receipt_backend_app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@receipt_backend_app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


VALID_THEMES = {"note", "memo", "poem"}
MAX_MESSAGE_LENGTH = 512


def parse_device_info(ua_string: str) -> str:
    """Parse User-Agent string into a short 'OS / Browser' string."""
    if "Windows NT" in ua_string:
        os_name = "Windows"
    elif "Macintosh" in ua_string or "Mac OS X" in ua_string:
        os_name = "macOS"
    elif "iPhone" in ua_string or "iPad" in ua_string:
        os_name = "iOS"
    elif "Android" in ua_string:
        os_name = "Android"
    elif "CrOS" in ua_string:
        os_name = "ChromeOS"
    elif "Linux" in ua_string:
        os_name = "Linux"
    else:
        os_name = "Unknown OS"

    if "Edg/" in ua_string or "EdgA/" in ua_string:
        browser = "Edge"
    elif "OPR/" in ua_string or "Opera" in ua_string:
        browser = "Opera"
    elif "Firefox/" in ua_string:
        browser = "Firefox"
    elif "Chrome/" in ua_string:
        browser = "Chrome"
    elif "Safari/" in ua_string:
        browser = "Safari"
    elif "MSIE" in ua_string or "Trident/" in ua_string:
        browser = "IE"
    else:
        browser = "Unknown Browser"

    return f"{os_name} / {browser}"


@receipt_backend_app.route("/print", methods=["POST"])
@limiter.limit("3 per minute")  # per-IP limit
def print_receipt():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    theme = data.get("theme")
    message = data.get("message")
    sender_name = data.get("sender_name", "")
    if not isinstance(sender_name, str):
        sender_name = ""
    sender_name = sender_name.strip()[:50]

    ip = request.remote_addr or "Unknown"
    device_info = parse_device_info(request.headers.get("User-Agent", ""))

    if not theme or not isinstance(theme, str) or theme not in VALID_THEMES:
        return jsonify({"error": "Invalid theme"}), 400

    if not message or not isinstance(message, str):
        return jsonify({"error": "No message provided"}), 400

    if len(message) > MAX_MESSAGE_LENGTH:
        # TODO: improve this error message
        return jsonify(
            {"error": f"Message exceeds {MAX_MESSAGE_LENGTH} character limit"}
        ), 400

    if message.count("\n") > 50:
        return jsonify({"error": "Message has too many line breaks (max 50)"}), 400

    try:
        subprocess.run(
            [
                "uv",
                "run",
                "--with",
                "escpos",
                os.path.join(os.path.dirname(__file__), "../../print/print_script.py"),
                theme,
                message,
                sender_name,
                ip,
                device_info,
            ],
            check=True,
            timeout=10,
        )
        return jsonify({"success": True, "message": "Message sent to printer!"})
    except subprocess.CalledProcessError:
        return jsonify({"error": "Print failed"}), 500
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Print timed out"}), 500


if __name__ == "__main__":
    # For local testing only — use Gunicorn in production
    receipt_backend_app.run(host="0.0.0.0", port=8000, debug=True)
