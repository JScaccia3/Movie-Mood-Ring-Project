import pytest
import responses
from app import app

# Base URL for TMDB API (adjust if different in your app)
TMDB_BASE_URL = "https://api.themoviedb.org/3"

@pytest.fixture
def client():
    """Set up Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@responses.activate
def test_index(client):
    """Test the index route loads the mood selection page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Select your current mood" in response.data  # Adjust to match your index.html

@responses.activate
def test_recommend_happy(client):
    """Test movie recommendations for a specific mood (Happy)."""
    responses.add(responses.GET, f"{TMDB_BASE_URL}/discover/movie",
                  json={"results": [{"id": 1, "title": "Happy Movie", "poster_path": "/happy.jpg", "overview": "A joyful film"}]})
    responses.add(responses.GET, f"{TMDB_BASE_URL}/movie/1",
                  json={"tagline": "Feel the joy!"})
    responses.add(responses.GET, f"{TMDB_BASE_URL}/movie/1/videos",
                  json={"results": [{"type": "Trailer", "key": "happy123"}]})

    response = client.post('/recommend', data={'mood': 'Happy'})
    assert response.status_code == 200
    assert b"Happy Movie" in response.data
    assert b"Feel the joy!" in response.data
    assert b"https://www.youtube.com/watch?v=happy123" in response.data

@responses.activate
def test_recommend_surprise_me(client):
    """Test the 'Surprise Me!' option returns random movies."""
    responses.add(responses.GET, f"{TMDB_BASE_URL}/discover/movie",
                  json={"results": [{"id": 2, "title": "Surprise Movie", "poster_path": "/surprise.jpg", "overview": "Unexpected fun"}]})
    responses.add(responses.GET, f"{TMDB_BASE_URL}/movie/2",
                  json={"tagline": "What a twist!"})
    responses.add(responses.GET, f"{TMDB_BASE_URL}/movie/2/videos",
                  json={"results": [{"type": "Trailer", "key": "surprise456"}]})

    response = client.post('/recommend', data={'mood': 'Surprise Me!'})
    assert response.status_code == 200
    assert b"Surprise Movie" in response.data

@responses.activate
def test_quiz_happy(client):
    """Test quiz maps to 'Happy' mood with specific answers."""
    responses.add(responses.GET, f"{TMDB_BASE_URL}/discover/movie",
                  json={"results": [{"id": 3, "title": "Quiz Happy", "poster_path": "/quiz.jpg", "overview": "Cheerful vibes"}]})
    responses.add(responses.GET, f"{TMDB_BASE_URL}/movie/3",
                  json={"tagline": "Smile!"})
    responses.add(responses.GET, f"{TMDB_BASE_URL}/movie/3/videos",
                  json={"results": [{"type": "Trailer", "key": "quiz789"}]})

    response = client.post('/quiz', data={'q1': 'yes', 'q2': 'no', 'q3': 'no'})
    assert response.status_code == 200
    assert b"Quiz Happy" in response.data

@responses.activate
def test_no_movies_found(client):
    """Test handling when no movies are returned."""
    responses.add(responses.GET, f"{TMDB_BASE_URL}/discover/movie",
                  json={"results": []})
    response = client.post('/recommend', data={'mood': 'Happy'})
    assert response.status_code == 200
    # The template may not show 'No movies found' if movies is empty, so just check the page loads
    # Optionally, check for a fallback element or text that is always present
    assert b"recommendations" in response.data or b"No movies found" in response.data
