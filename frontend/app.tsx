import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const response = await axios.get('/api/items');
      setItems(response.data);
      setLoading(false);
    } catch (error) {
      console.error(error);
    }
  };

  const handleNewItemChange = (event) => {
    setNewItem(event.target.value);
  };

  const handleNewItemSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post('/api/items', { name: newItem });
      setNewItem('');
      fetchItems();
    } catch (error) {
      console.error(error);
    }
  };

  const handleLike = async (itemId) => {
    try {
      await axios.post(`/api/items/${itemId}/like`);
      fetchItems();
    } catch (error) {
      console.error(error);
    }
  };

  const handleComment = async (itemId, comment) => {
    try {
      await axios.post(`/api/items/${itemId}/comment`, { comment });
      fetchItems();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <header>
        <h1>Collaborative Platform</h1>
      </header>
      <main>
        <form onSubmit={handleNewItemSubmit}>
          <label htmlFor="newItem">New Item:</label>
          <input
            type="text"
            id="newItem"
            value={newItem}
            onChange={handleNewItemChange}
          />
          <button type="submit">Add Item</button>
        </form>
        {loading ? (
          <p>Loading...</p>
        ) : (
          items.map((item) => (
            <div key={item.id} className="item">
              <h2>{item.name}</h2>
              <p>Likes: {item.likes}</p>
              <div className="actions">
                <button onClick={() => handleLike(item.id)}>Like</button>
              </div>
              <div className="comments">
                {item.comments.map((comment) => (
                  <div key={comment.id} className="comment">
                    <p>{comment.text}</p>
                  </div>
                ))}
              </div>
              <form
                onSubmit={(event) => {
                  event.preventDefault();
                  handleComment(item.id, event.target.comment.value);
                  event.target.comment.value = '';
                }}
              >
                <label htmlFor="comment">Add Comment:</label>
                <input type="text" id="comment" />
                <button type="submit">Submit</button>
              </form>
            </div>
          ))
        )}
      </main>
      <footer>
        <p>&copy; 2022 Collaborative Platform</p>
      </footer>
    </div>
  );
};

export default App;

