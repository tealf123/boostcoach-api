"""
BoostCoach API - Rocket League AI Coaching Platform
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp/boostcoach'

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage
analyses_store = {}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/', methods=['GET'])
def index():
    return '''<html><body><h1>BoostCoach API</h1><p>Running</p></body></html>''', 200

# Import routes (after app init)
try:
    from routes import replay, coaching
    app.register_blueprint(replay.bp)
    app.register_blueprint(coaching.bp)
except Exception as e:
    print(f"Warning: Could not import routes: {e}")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
