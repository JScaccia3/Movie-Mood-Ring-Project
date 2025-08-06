from app import app
import pytest

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"The Movie Mood Ring" in response.data

def test_recommend_page_valid_mood(client):
    """Test that the recommend page works with a valid mood."""
    response = client.post('/recommend', data={'mood': 'happy'})
    assert response.status_code == 200
    assert b"Recommendations for Happy Mood" in response.data

def test_recommend_page_invalid_mood(client):
    """Test that the recommend page handles invalid moods."""
    response = client.post('/recommend', data={'mood': 'invalid'})
    assert response.status_code == 200
    assert b"Mood not recognized" in response.data
    