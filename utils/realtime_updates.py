from flask_socketio import emit

def handle_like(socketio, item_id):
    item = Item.query.get(item_id)
    if item:
        item.likes += 1
        db.session.commit()
        emit('item_updated', {'id': item.id, 'likes': item.likes}, broadcast=True)
    else:
        emit('error', {'message': 'Item not found'})

def handle_comment(socketio, item_id, comment):
    item = Item.query.get(item_id)
    if item:
        comment = Comment(text=comment, item=item)
        db.session.add(comment)
        db.session.commit()
        emit('item_updated', {'id': item.id, 'comments': [{'id': comment.id, 'text': comment.text}]}, broadcast=True)
    else:
        emit('error', {'message': 'Item not found'})

