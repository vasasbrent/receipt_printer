from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess

receipt_backend_app = Flask(__name__)

# Configure Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    receipt_backend_app=receipt_backend_app,
    default_limits=["10 per minute"],  # global fallback
)


@receipt_backend_app.route('/print', methods=['POST'])
@limiter.limit("3 per minute")  # per-IP limit
def print_receipt():
    data = request.get_json()
    theme = data.get('theme')
    message = data.get('message')

    if not theme or not message:
        return jsonify({"error": "No message provided"}), 400

    # Example call to your Python print script
    try:
        subprocess.run(["python3", "/home/brentvasas/documents/projects/print_script.py", theme, message], check=True)
        return jsonify({'success': True, 'message': 'Message sent to printer'})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Print failed: {e}"}), 500



if __name__ == '__main__':
    # For local testing only — use Gunicorn in production
    receipt_backend_app.run(host='0.0.0.0', port=8000, debug=True)
