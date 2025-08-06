import os
import random
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Define moods
moods = [
    "Happy", "Sad", "Excited", "Scared", "Hungry", "Relaxed", "Romantic", "Inspired",
    "Nostalgic", "Curious", "Adventurous", "Angry", "Hopeful", "Mellow", "Playful",
    "Tense", "Cozy", "Epic", "Silly", "Reflective", "Energetic", "Surprise Me!",
    "Spooky Halloween", "Christmas", "Valentine’s Day", "Beachy Teen Summer"
]

# Mood to keyword mapping with actual TMDB keyword IDs
mood_to_keywords = {
    'Happy': [304995, 334465, 322268],
    'Sad': [351091, 325854, 316421],
    'Excited': [274978, 353406, 322942],
    'Scared': [315058, 288394, 316362],
    'Hungry': [10637, 1918, 1946],
    'Relaxed': [209673, 303381, 282080],
    'Romantic': [9673, 9840, 324429],
    'Inspired': [328417, 191446, 345513],
    'Nostalgic': [5609, 324700, 338880],
    'Curious': [316332, 242691],
    'Adventurous': [322942, 4759, 6917],
    'Angry': [321464, 9748, 322496],
    'Hopeful': [325840, 319357, 355425],
    'Mellow': [269808, 303381],
    'Playful': [316433, 288816, 319320],
    'Tense': [314730, 318868, 316362],
    'Cozy': [355748, 317983, 325784],
    'Epic': [291153],
    'Silly': [355720, 309974, 337970],
    'Reflective': [269808, 212737, 278680],
    'Energetic': [325856, 267944, 326457],
    'Spooky Halloween': [3335, 333978, 315058],
    'Christmas': [207317, 65, 221602],
    'Valentine’s Day': [9673, 9840, 251912],
    'Beachy Teen Summer': [13088, 966, 346617]
}

def get_movies_for_mood(mood, language='en', min_rating=7.0):
    if mood == "Surprise Me!":
        selected_mood = random.choice([m for m in moods if m != "Surprise Me!"])
        keywords = mood_to_keywords[selected_mood]
    else:
        keywords = mood_to_keywords.get(mood, [])

    params = {
        "api_key": TMDB_API_KEY,
        "include_adult": False,
        "with_original_language": language,
        "vote_average.gte": min_rating,
        "sort_by": "popularity.desc"
    }

    if keywords:
        params["with_keywords"] = "|".join(map(str, keywords))

    response = requests.get(f"{TMDB_BASE_URL}/discover/movie", params=params)
    movies = response.json().get("results", [])

    selected_movies = random.sample(movies, min(5, len(movies))) if movies else []

    for movie in selected_movies:
        details_response = requests.get(f"{TMDB_BASE_URL}/movie/{movie['id']}?api_key={TMDB_API_KEY}")
        details = details_response.json()
        movie['fun_fact'] = details.get("tagline", "No tagline available.")

        video_response = requests.get(f"{TMDB_BASE_URL}/movie/{movie['id']}/videos?api_key={TMDB_API_KEY}")
        videos = video_response.json().get("results", [])
        trailer = next((v for v in videos if v["type"] == "Trailer"), None)
        movie['trailer_url'] = f"https://www.youtube.com/watch?v={trailer['key']}" if trailer else None

    return selected_movies, mood

@app.route('/')
def index():
    return render_template('index.html', moods=moods)

@app.route('/recommend', methods=['POST'])
def recommend():
    mood = request.form.get('mood')
    language = request.form.get('language', 'en')
    min_rating = float(request.form.get('min_rating', 7.0))
    selected_movies, mood = get_movies_for_mood(mood, language, min_rating)
    return render_template('recommendations.html', movies=selected_movies, mood=mood)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        q1 = request.form.get('q1')  # Uplifting?
        q2 = request.form.get('q2')  # Scary?
        q3 = request.form.get('q3')  # Romantic?
        
        if q1 == 'yes':
            mood = "Happy"
        elif q2 == 'yes':
            mood = "Scared"
        elif q3 == 'yes':
            mood = "Romantic"
        else:
            mood = "Relaxed"
        
        selected_movies, mood = get_movies_for_mood(mood, 'en', 7.0)
        return render_template('recommendations.html', movies=selected_movies, mood=mood)
    
    return render_template('quiz.html')

if __name__ == "__main__":
    app.run(debug=True)