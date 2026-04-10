from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from coaching_engine import generate_coaching_report
import traceback
from uuid import uuid4

bp = Blueprint('replay', __name__, url_prefix='/api/replays')

@bp.route('/upload', methods=['POST'])
def upload_replay():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.replay'):
            return jsonify({'error': 'Only .replay files allowed'}), 400
        
        # Read file
        replay_bytes = file.read()
        
        # Generate coaching
        result = generate_coaching_report(replay_bytes, file.filename)
        if result['status'] != 'success':
            return jsonify({'error': 'Coaching generation failed'}), 500
        
        # Store in memory
        from app import analyses_store
        aid = str(uuid4())
        analyses_store[aid] = {
            'filename': file.filename,
            'report': result['report'],
            'size': len(replay_bytes)
        }
        
        return jsonify({
            'status': 'success',
            'analysis_id': aid,
            'coaching_report': result['report']
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
