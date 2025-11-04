from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from your front end

# POST endpoint to send message
@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    theme = data.get('theme')
    message = data.get('message')

    if not theme or not message:
        return jsonify({'success': False, 'error': 'Theme and message are required'}), 400

    # Call your printing script with arguments
    try:
        # Example: call print_script.py with theme and message as args
        subprocess.run(
            ['python3', 'print_script.py', theme, message],
            check=True
        )
        return jsonify({'success': True, 'message': 'Message sent to printer'})
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
