import pytest
import os
from app import app

TMDB_BASE_URL = "https://api.themoviedb.org/3"

@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setitem(os.environ, "TMDB_API_KEY", "test_api_key")

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Select your current mood" in response.data

def test_recommend_happy(client):
    response = client.post('/recommend', data={'mood': 'Happy', 'language': 'en', 'min_rating': '7.0'})
    assert response.status_code == 200

def test_recommend_surprise_me(client):
    response = client.post('/recommend', data={'mood': 'Surprise Me!', 'language': 'en', 'min_rating': '7.0'})
    assert response.status_code == 200

def test_quiz_happy(client):
    response = client.post('/quiz', data={'q1': 'yes', 'q2': 'no', 'q3': 'no'})
    assert response.status_code == 200

def test_no_movies_found(client):
    response = client.post('/recommend', data={'mood': 'Happy', 'language': 'en', 'min_rating': '7.0'})
    assert response.status_code == 200