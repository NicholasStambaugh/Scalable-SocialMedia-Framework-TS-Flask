backend/api.py

from flask import Blueprint, request, jsonify
from .database import db, Item, Comment

api_bp = Blueprint('api', __name__)

@api_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'likes': item.likes,
        'comments': [{
            'id': comment.id,
            'text': comment.text
        } for comment in item.comments]
    } for item in items])

@api_bp.route('/items', methods=['POST'])
def create_item():
    name = request.json.get('name')
    item = Item(name=name)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully'})

@api_bp.route('/items/<int:item_id>/like', methods=['POST'])
def like_item(item_id):
    item = Item.query.get(item_id)
    if item:
        item.likes += 1
        db.session.commit()
        return jsonify({'message': 'Item liked successfully'})
    return jsonify({'message': 'Item not found'})

@api_bp.route('/items/<int:item_id>/comment', methods=['POST'])
def add_comment(item_id):
    item = Item.query.get(item_id)
    if item:
        text = request.json.get('comment')
        comment = Comment(text=text, item=item)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'Comment added successfully'})
    return jsonify({'message': 'Item not found'})

