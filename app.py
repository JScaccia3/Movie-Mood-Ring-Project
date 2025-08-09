import os
import random
import requests
from flask import Flask, render_template, request, session
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Define moods
moods = [
    "Happy", "Sad", "Excited", "Scared", "Hungry", "Relaxed", "Romantic", "Inspired",
    "Nostalgic", "Curious", "Adventurous", "Angry", "Hopeful", "Mellow", "Playful",
    "Tense", "Cozy", "Epic", "Silly", "Reflective", "Energetic",
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

# Custom filter for number formatting
@app.template_filter('format_number')
def format_number(value):
    return "{:,}".format(value)

def get_random_posters(count=8):
    if 'index_posters' in session:
        return session['index_posters']
    params = {
        "api_key": TMDB_API_KEY,
        "include_adult": False,
        "sort_by": "popularity.desc",
        "page": random.randint(1, 10)
    }
    response = requests.get(f"{TMDB_BASE_URL}/discover/movie", params=params)
    movies = response.json().get("results", [])
    selected_movies = random.sample(movies, min(count, len(movies))) if movies else []
    posters = [movie["poster_path"] for movie in selected_movies if movie.get("poster_path")]
    session['index_posters'] = posters
    return posters

def get_movies_for_mood(mood, language='en', min_rating=7.0, use_session=True):
    if mood == "Surprise Me!":
        selected_mood = random.choice([m for m in moods if m != "Surprise Me!"])
        keywords = mood_to_keywords[selected_mood]
    else:
        selected_mood = mood
        keywords = mood_to_keywords.get(mood, [])

    if selected_mood not in moods:
        selected_mood = "Happy"

    session_key = f"movies_{selected_mood}"
    if use_session and session_key in session:
        movie_ids = session[session_key]
        movies = []
        for movie_id in movie_ids:
            details_response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=videos")
            details = details_response.json() if details_response.status_code == 200 else {}
            movies.append(details)
    else:
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
        movies = random.sample(movies, min(8, len(movies))) if movies else []
        session[session_key] = [movie["id"] for movie in movies]

    selected_movies = []
    for movie in movies:
        trailer = next((v for v in movie.get("videos", {}).get("results", []) if v["type"] == "Trailer" and v["site"] == "YouTube"), None)
        selected_movies.append({
            "id": movie.get("id"),
            "title": movie.get("title", "Unknown Title"),
            "poster_path": movie.get("poster_path", ""),
            "overview": movie.get("overview", "No overview available."),
            "vote_average": movie.get("vote_average", 0.0),
            "vote_count": movie.get("vote_count", 0),
            "trailer_url": f"https://www.youtube.com/watch?v={trailer['key']}" if trailer else None
        })

    return selected_movies, selected_mood

@app.route('/')
def index():
    posters = get_random_posters(8)
    return render_template('index.html', moods=moods, posters=posters)

@app.route('/recommend', methods=['POST'])
def recommend():
    mood = request.form.get('mood')
    language = request.form.get('language', 'en')
    min_rating = float(request.form.get('min_rating', 7.0))
    session.pop(f"movies_{mood}", None)
    selected_movies, mood = get_movies_for_mood(mood, language, min_rating)
    posters = get_random_posters(8)
    return render_template('recommendations.html', movies=selected_movies, mood=mood, posters=posters)

@app.route('/recommend/<mood>', methods=['GET'])
def recommend_get(mood):
    selected_movies, mood = get_movies_for_mood(mood, use_session=True)
    posters = get_random_posters(8)
    return render_template('recommendations.html', movies=selected_movies, mood=mood, posters=posters)


#Quiz

quiz_questions = [
    {
        "questions": "q1",
        "options": {"beach": ["Happy", "Nostalgic", "Hopeful", "Silly", "Reflective", "Beachy Teen Summer"], 
                    "mountains": ["Sad", "Scared", "Adventurous", "Angry", "Energetic", "Spooky Halloween"], 
                    "city": ["Excited", "Inspired", "Curious", "Tense", "Epic", "Christmas"], 
                    "staycation": ["Romantic", "Hungry", "Mellow", "Playful", "Cozy", "Valentine’s Day"]}
    },
    {
        "questions": "q2",
        "options": {"popcorn": ["Sad", "Hungry", "Silly", "Christmas", "Scared", "Angry"], 
                    "chocolate": ["Romantic", "Mellow", "Playful", "Cozy", "Reflective", "Valentine’s Day"], 
                    "candy": ["Excited", "Nostalgic", "Curious", "Adventurous", "Energetic", "Spooky Halloween"], 
                    "fruits": ["Happy", "Inspired", "Hopeful", "Tense", "Epic", "Beachy Teen Summer"]}
    },
    {
        "questions": "q3",
        "options": {"party": ["Excited", "Beachy Teen Summer", "Angry", "Energetic", "Curious", "Tense"], 
                    "takeout & movie": ["Romantic", "Hopeful", "Scared", "Hungry", "Relaxed", "Valentine’s Day"], 
                    "reading": ["Sad", "Nostalgic", "Reflective", "Mellow", "Cozy", "Christmas"], 
                    "gaming": ["Happy", "Silly", "Adventurous", "Playful", "Spooky Halloween", "Inspired"]}
    }
]

@app.route('/surprise')
def surprise():
    selected_movies, mood = get_movies_for_mood("Surprise Me!", 'en', 7.0)
    return render_template('recommendations.html', movies=selected_movies, mood="Surprise Me!")

#Quiz

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        mood_score = {mood: 0 for mood in moods}
        answers = {
            "q1": request.form.get('q1'),
            "q2": request.form.get('q2'),
            "q3": request.form.get('q3')
        } 
        for q in quiz_questions:
            question_list = q["questions"]
            answer = answers.get(question_list)
            if answer in q["options"]:
                for mood in q["options"][answer]:
                    mood_score[mood] += 1
        max_score = max(mood_score.values())
        top_moods = [m for m, score in mood_score.items() if score == max_score and score > 0]
        final_mood = top_moods[0] if top_moods else "Relaxed"
        
        selected_movies, mood = get_movies_for_mood(final_mood, 'en', 7.0)
        return render_template('recommendations.html', movies=selected_movies, mood= final_mood)
    
    return render_template('quiz.html')

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=videos")
    details = response.json() if response.status_code == 200 else {}
    
    trailer = next((v for v in details.get("videos", {}).get("results", []) if v["type"] == "Trailer" and v["site"] == "YouTube"), None)
    
    budget = details.get("budget", 0)
    revenue = details.get("revenue", 0)
    
    movie = {
        "id": details.get("id", movie_id),
        "title": details.get("title", "Unknown Title"),
        "poster_path": details.get("poster_path", ""),
        "overview": details.get("overview", "No overview available."),
        "vote_average": details.get("vote_average", 0.0),
        "vote_count": details.get("vote_count", 0),
        "genres": ", ".join(g["name"] for g in details.get("genres", [])) or "Unknown",
        "runtime": details.get("runtime", 0),
        "release_date": details.get("release_date", "Unknown"),
        "production_companies": ", ".join(c["name"] for c in details.get("production_companies", [])) or "Unknown",
        "budget": "N/A" if budget == 0 else "${:,}".format(budget),
        "revenue": "N/A" if revenue == 0 else "${:,}".format(revenue),
        "trailer_url": f"https://www.youtube.com/watch?v={trailer['key']}" if trailer else None
    }
    
    mood = request.args.get('mood', 'Happy')
    if mood not in moods:
        mood = 'Happy'
    posters = get_random_posters(8)
    return render_template('movie_details.html', movie=movie, mood=mood, posters=posters)

if __name__ == "__main__":
    app.run(debug=True)

    