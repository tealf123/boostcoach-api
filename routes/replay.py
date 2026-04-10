"""
Replay upload and processing routes
"""

from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from carball_parser import parse_replay
from coaching_engine import generate_coaching_report
from database import get_db_cursor
import json

bp = Blueprint('replay', __name__, url_prefix='/api/replays')

ALLOWED_EXTENSIONS = {'replay'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_replay():
    """Upload and process a replay file"""
    try:
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only .replay files allowed'}), 400
    
    try:
        # For now, assume user_id is 1 (auth not yet implemented)
        user_id = request.form.get('user_id', 1)
        
        # Save file
        filename = secure_filename(file.filename)
        replay_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(replay_path)
        
        # Parse replay with Carball
        parsed_result = parse_replay(replay_path)
        
        if parsed_result['status'] != 'success':
            return jsonify({
                'error': 'Failed to parse replay',
                'details': parsed_result.get('error')
            }), 400
        
        # Generate coaching report
        parsed_data = json.loads(parsed_result['raw_data'])
        coaching_result = generate_coaching_report(parsed_data)
        
        if coaching_result['status'] != 'success':
            return jsonify({
                'error': 'Failed to generate coaching report',
                'details': coaching_result.get('error')
            }), 500
        
        coaching_report = coaching_result['report']
        
        # Store in database
        with get_db_cursor() as cursor:
            cursor.execute('''
                INSERT INTO analyses 
                (user_id, replay_filename, replay_raw_path, parsed_data, coaching_report)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, filename, replay_path, parsed_result['raw_data'], coaching_report))
            
            analysis_id = cursor.lastrowid
        
        return jsonify({
            'status': 'success',
            'analysis_id': analysis_id,
            'replay_filename': filename,
            'coaching_report': coaching_report,
            'parsed_summary': parsed_result['summary']
        }), 201
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return jsonify({'error': str(e), 'trace': error_trace}), 500

@bp.route('', methods=['GET'])
def list_analyses():
    """List user's analyses"""
    user_id = request.args.get('user_id', 1)  # TODO: Get from auth token
    
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT id, replay_filename, created_at FROM analyses
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        analyses = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({'analyses': analyses}), 200

@bp.route('/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get a specific analysis and coaching report"""
    
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT id, replay_filename, parsed_data, coaching_report, created_at
            FROM analyses WHERE id = ?
        ''', (analysis_id,))
        
        row = cursor.fetchone()
        
        if not row:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis = {
            'id': row['id'],
            'replay_filename': row['replay_filename'],
            'parsed_data': json.loads(row['parsed_data']),
            'coaching_report': row['coaching_report'],
            'created_at': row['created_at']
        }
    
    return jsonify(analysis), 200
