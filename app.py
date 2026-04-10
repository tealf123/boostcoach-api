"""
BoostCoach API - Rocket League AI Coaching Platform
Main Flask application
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATABASE'] = 'boostcoach.db'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
from database import init_db
init_db()

# Import routes
from routes import auth, replay, coaching

app.register_blueprint(auth.bp)
app.register_blueprint(replay.bp)
app.register_blueprint(coaching.bp)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
