from movie_api import get_movies_by_mood
import pytest

def test_valid_mood():
    """Test getting movies for a valid mood."""
    results = get_movies_by_mood('happy')
    assert isinstance(results, list)
    assert len(results) <= 5
    assert all('title' in movie and 'poster' in movie and 'overview' in movie and 'fun_fact' in movie for movie in results)

def test_invalid_mood():
    """Test handling of an invalid mood."""
    result = get_movies_by_mood('invalid')
    assert result == {"error": "Mood not recognized."}

def test_surprise_mood():
    """Test getting movies for the 'surprise' mood."""
    results = get_movies_by_mood('surprise')
    assert isinstance(results, list)
    assert len(results) <= 5
    assert all('title' in movie and 'poster' in movie and 'overview' in movie and 'fun_fact' in movie for movie in results)