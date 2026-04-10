"""
BoostCoach API - Rocket League AI Coaching Platform
Main Flask application
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from uuid import uuid4
import io

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp/boostcoach'

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage for MVP
analyses_store = {}

@app.route('/', methods=['GET'])
def index():
    try:
        with open('index.html', 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except:
        return jsonify({'status': 'boostcoach api running'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

# Import routes
from routes import replay, coaching

app.register_blueprint(replay.bp)
app.register_blueprint(coaching.bp)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
