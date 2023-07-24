utils/validation.py

from flask import request, jsonify
from functools import wraps
from backend.database import User

def validate_json(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({'message': 'Invalid JSON format'}), 400
            for field, field_type in schema.items():
                if field not in request.json or not isinstance(request.json[field], field_type):
                    return jsonify({'message': f'Invalid {field} field'}), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_user_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return func(*args, **kwargs)
    return wrapper

def validate_item_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        item_id = kwargs.get('item_id')
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'message': 'Item not found'}), 404
        return func(*args, **kwargs)
    return wrapper

