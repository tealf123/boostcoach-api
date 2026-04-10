"""
Interactive coaching Q&A routes
"""

from flask import Blueprint, request, jsonify
from coaching_engine import generate_qa_response
import traceback

bp = Blueprint('coaching', __name__, url_prefix='/api/analyses')

@bp.route('/<analysis_id>/ask', methods=['POST'])
def ask_question(analysis_id):
    """Ask a question about the match"""
    from app import analyses_store
    
    if analysis_id not in analyses_store:
        return jsonify({'error': 'Analysis not found'}), 404
    
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        coaching_report = analyses_store[analysis_id]['coaching_report']
        
        # Generate Q&A response
        response_result = generate_qa_response(coaching_report, question)
        
        if response_result['status'] != 'success':
            return jsonify({
                'error': 'Failed to generate response',
                'details': response_result.get('error')
            }), 500
        
        return jsonify({
            'status': 'success',
            'question': question,
            'response': response_result['response']
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@bp.route('/<analysis_id>/conversation', methods=['GET'])
def get_conversation(analysis_id):
    """Get conversation history (MVP: empty for now)"""
    from app import analyses_store
    
    if analysis_id not in analyses_store:
        return jsonify({'error': 'Analysis not found'}), 404
    
    return jsonify({'conversation': []}), 200
