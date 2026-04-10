"""
Replay upload and processing routes
"""

from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from carball_parser import parse_replay
from coaching_engine import generate_coaching_report
import json
import traceback
from uuid import uuid4

bp = Blueprint('replay', __name__, url_prefix='/api/replays')

ALLOWED_EXTENSIONS = {'replay'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_replay():
    """Upload and process a replay file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .replay files allowed'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        replay_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(replay_path)
        
        # Read replay bytes
        with open(replay_path, 'rb') as f:
            replay_bytes = f.read()
        
        # Generate coaching report
        coaching_result = generate_coaching_report(replay_bytes, filename)
        
        if coaching_result['status'] != 'success':
            return jsonify({
                'error': 'Failed to generate coaching report',
                'details': coaching_result.get('error')
            }), 500
        
        coaching_report = coaching_result['report']
        
        # Store in memory (MVP)
        from app import analyses_store
        analysis_id = str(uuid4())
        analyses_store[analysis_id] = {
            'filename': filename,
            'coaching_report': coaching_report,
            'file_size': len(replay_bytes)
        }
        
        return jsonify({
            'status': 'success',
            'analysis_id': analysis_id,
            'replay_filename': filename,
            'coaching_report': coaching_report,
            'parsed_summary': {'file_size': len(replay_bytes)}
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@bp.route('', methods=['GET'])
def list_analyses():
    """List analyses"""
    from app import analyses_store
    return jsonify({'analyses': list(analyses_store.keys())}), 200

@bp.route('/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get a specific analysis"""
    from app import analyses_store
    
    if analysis_id not in analyses_store:
        return jsonify({'error': 'Analysis not found'}), 404
    
    data = analyses_store[analysis_id]
    return jsonify({
        'id': analysis_id,
        'replay_filename': data['filename'],
        'coaching_report': data['coaching_report'],
        'file_size': data['file_size']
    }), 200
