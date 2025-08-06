from tmdbv3api import TMDb, Discover
from dotenv import load_dotenv
import os
import random
from typing import List, Any, Union  # Add Union for return type

load_dotenv()
tmdb = TMDb()
tmdb.api_key = os.getenv('TMDB_API_KEY')

mood_to_genre = {
    'happy': [35, 10751, 16],  # Comedy, Family, Animation
    'sad': [18, 10749],        # Drama, Romance
    'scary': [27, 53],         # Horror, Thriller
    'excited': [28, 12]        # Action, Adventure
}

def get_movies_by_mood(mood: str, num_recommendations: int = 5) -> Union[List[dict], dict]:
    """Fetch movies based on user mood with randomization.

    Args:
        mood (str): User's selected mood (e.g., 'happy', 'surprise').
        num_recommendations (int): Number of movies to return (default: 5).

    Returns:
        Union[List[dict], dict]: List of movie dictionaries or error dictionary.
    """
    if mood not in mood_to_genre and mood != 'surprise':
        return {"error": "Mood not recognized."}

    discover = Discover()
    if mood == 'surprise':
        genres = [g for sublist in mood_to_genre.values() for g in sublist]
    else:
        genres = mood_to_genre[mood]

    try:
        movies: List[Any] = discover.discover_movies(params={'with_genres': ','.join(map(str, genres))})  # type: ignore
        random.shuffle(movies)  # type: ignore
        results = []
        for m in movies[:num_recommendations]:
            results.append({
                'title': m.title,  # type: ignore
                'poster': f"https://image.tmdb.org/t/p/w500{m.poster_path}" if m.poster_path else None,  # type: ignore
                'overview': m.overview,  # type: ignore
                'fun_fact': get_movie_fun_fact(m.id)  # type: ignore
            })
        return results
    except Exception as e:
        return {"error": f"Error fetching movies: {str(e)}"}

def get_movie_fun_fact(movie_id: int) -> str:
    """Fetch a fun fact about the movie (mocked for simplicity).

    Args:
        movie_id (int): TMDB movie ID.

    Returns:
        str: A fun fact about the movie.
    """
    return f"Did you know? This movie (ID: {movie_id}) has an interesting story behind its production!"