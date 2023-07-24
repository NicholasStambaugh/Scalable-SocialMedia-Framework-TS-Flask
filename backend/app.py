from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='item', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

# Routes
@app.route('/api/items', methods=['GET'])
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

@app.route('/api/items', methods=['POST'])
def create_item():
    name = request.json.get('name')
    item = Item(name=name)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully'})

@app.route('/api/items/<int:item_id>/like', methods=['POST'])
def like_item(item_id):
    item = Item.query.get(item_id)
    if item:
        item.likes += 1
        db.session.commit()
        return jsonify({'message': 'Item liked successfully'})
    return jsonify({'message': 'Item not found'})

@app.route('/api/items/<int:item_id>/comment', methods=['POST'])
def add_comment(item_id):
    item = Item.query.get(item_id)
    if item:
        text = request.json.get('comment')
        comment = Comment(text=text, item=item)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'Comment added successfully'})
    return jsonify({'message': 'Item not found'})

# SocketIO Events
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)

