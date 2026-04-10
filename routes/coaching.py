"""
Interactive coaching Q&A routes
"""

from flask import Blueprint, request, jsonify
from coaching_engine import generate_qa_response
from database import get_db_cursor
import json

bp = Blueprint('coaching', __name__, url_prefix='/api/analyses')

@bp.route('/<int:analysis_id>/ask', methods=['POST'])
def ask_question(analysis_id):
    """Ask a question about the match"""
    
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Get analysis and coaching report
        with get_db_cursor() as cursor:
            cursor.execute('''
                SELECT parsed_data, coaching_report FROM analyses WHERE id = ?
            ''', (analysis_id,))
            
            row = cursor.fetchone()
            
            if not row:
                return jsonify({'error': 'Analysis not found'}), 404
            
            parsed_data = json.loads(row['parsed_data'])
            coaching_report = row['coaching_report']
        
        # Generate Q&A response
        response_result = generate_qa_response(parsed_data, coaching_report, question)
        
        if response_result['status'] != 'success':
            return jsonify({
                'error': 'Failed to generate response',
                'details': response_result.get('error')
            }), 500
        
        # Store conversation in database
        coach_response = response_result['response']
        with get_db_cursor() as cursor:
            cursor.execute('''
                INSERT INTO conversations (analysis_id, user_message, coach_response)
                VALUES (?, ?, ?)
            ''', (analysis_id, question, coach_response))
        
        return jsonify({
            'status': 'success',
            'question': question,
            'response': coach_response
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:analysis_id>/conversation', methods=['GET'])
def get_conversation(analysis_id):
    """Get full Q&A conversation history for an analysis"""
    
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT user_message, coach_response, created_at
            FROM conversations
            WHERE analysis_id = ?
            ORDER BY created_at ASC
        ''', (analysis_id,))
        
        messages = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({'conversation': messages}), 200
