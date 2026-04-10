"""
Authentication routes (placeholder for MVP)
Full auth implementation comes after core pipeline is working
"""

from flask import Blueprint, request, jsonify
from database import get_db_cursor

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    """User signup (placeholder)"""
    # TODO: Implement with bcrypt and JWT
    return jsonify({'message': 'Auth not yet implemented'}), 501

@bp.route('/login', methods=['POST'])
def login():
    """User login (placeholder)"""
    # TODO: Implement with JWT tokens
    return jsonify({'message': 'Auth not yet implemented'}), 501

@bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current authenticated user (placeholder)"""
    # TODO: Extract and validate JWT token
    return jsonify({'message': 'Auth not yet implemented'}), 501
