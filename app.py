from flask import Flask, render_template, request
from movie_api import get_movies_by_mood

app = Flask(__name__)

@app.route('/')
def index():
    """Render the home page with mood selection."""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """Handle mood submission and display recommendations."""
    mood = request.form.get('mood')
    if mood is None:
        return render_template('recommendations.html', mood='unknown', recommendations={"error": "No mood selected."})
    recommendations = get_movies_by_mood(mood)
    return render_template('recommendations.html', mood=mood, recommendations=recommendations)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)