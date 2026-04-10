from flask import Blueprint, request, jsonify
from coaching_engine import generate_qa_response

bp = Blueprint('coaching', __name__, url_prefix='/api/analyses')

@bp.route('/<aid>/ask', methods=['POST'])
def ask_question(aid):
    try:
        from app import analyses_store
        if aid not in analyses_store:
            return jsonify({'error': 'Not found'}), 404
        
        data = request.get_json()
        q = data.get('question', '')
        if not q:
            return jsonify({'error': 'No question'}), 400
        
        report = analyses_store[aid]['report']
        result = generate_qa_response(report, q)
        
        if result['status'] != 'success':
            return jsonify({'error': 'Failed'}), 500
        
        return jsonify({
            'question': q,
            'response': result['response']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
