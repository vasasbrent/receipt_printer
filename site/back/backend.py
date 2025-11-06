from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess

app = Flask(__name__)

# Configure Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["10 per minute"],  # global fallback
)


@app.route('/print', methods=['POST'])
@limiter.limit("3 per minute")  # per-IP limit
def print_receipt():
    data = request.get_json() or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Example call to your Python print script
    try:
        subprocess.run(["/usr/bin/python3", "/path/to/your/print_script.py", message], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Print failed: {e}"}), 500

    return jsonify({"status": "Message sent!", "message": message})


if __name__ == '__main__':
    # For local testing only — use Gunicorn in production
    app.run(host='0.0.0.0', port=8000, debug=True)
