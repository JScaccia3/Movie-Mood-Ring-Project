# Movie Mood Ring 🎥✨

Welcome to **Movie Mood Ring**, a Flask-based web app that recommends movies tailored to your current mood! Powered by the [TMDb API](https://www.themoviedb.org/), this app lets you select from a variety of moods and discover films that match your vibe. Whether you're feeling cozy or adventurous, Movie Mood Ring has you covered with personalized recommendations.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Local Setup with Conda](#local-setup-with-conda)
- [Deploying on Render.com](#deploying-on-rendercom)
- [Running Tests](#running-tests)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Mood-Based Recommendations**: Choose from 26 unique moods to get curated movie suggestions.
- **Randomized Results**: Get fresh movie picks every time, even for the same mood.
- **Fun Extras**: Enjoy movie taglines as fun facts and watch trailers via YouTube links.
- **Mood Quiz**: Not sure how you feel? Take a quick quiz to find your movie mood!
- **Responsive Design**: A sleek, cinematic interface that looks great on any device.

## Prerequisites
Before you start, ensure you have:
- A [TMDb API key](https://www.themoviedb.org/settings/api) (free to obtain by signing up).
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) installed (Miniconda or Anaconda).
- Git installed to clone the repository.
- A Render.com account for deployment (optional).

## Local Setup with Conda
Follow these steps to run the app locally using Conda:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/movie-mood-ring.git
   cd movie-mood-ring
   ```

2. **Create a Conda Environment**:
   Create a new environment named `movie_mood_ring` with Python 3.9:
   ```bash
   conda create -n movie_mood_ring python=3.9
   ```

3. **Activate the Environment**:
   ```bash
   conda activate movie_mood_ring
   ```

4. **Install Dependencies**:
   Install required packages from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   Ensure `requirements.txt` includes:
   ```
   Flask
   requests
   python-dotenv
   gunicorn
   ```

5. **Set Up the TMDb API Key**:
   You can configure the API key in one of two ways:

   - **Option 1: Using a `.env` File** (Recommended):
     Create a `.env` file in the project root:
     ```bash
     echo "TMDB_API_KEY=your_api_key_here" > .env
     ```
     Replace `your_api_key_here` with your actual TMDb API key.

   - **Option 2: Using a Command-Line Environment Variable**:
     Set the API key directly in your terminal before running the app:

     To set your TMDB API key in the command line so your Flask app can access it, use this PowerShell command before running your app:

     $env:TMDB_API_KEY = "your_actual_tmdb_api_key"

     Replace "your_actual_tmdb_api_key" with your real TMDB API key (including quotes).
     
     Then, in the same terminal session, run:
     $env:FLASK_APP = "app.py"
     flask run

This will ensure your app can read the API key from the environment.


6. **Run the Application**:
   Start the Flask development server:
   ```bash
   flask run
   ```
   Or, use Python directly:
   ```bash
   python app.py
   ```

7. **Access the App**:
   Open your browser and navigate to `http://localhost:5000`.

## Deploying on Render.com
To deploy the app on Render.com for public access:

1. **Create a Render Account**:
   Sign up at [Render.com](https://render.com/) and log in.

2. **Set Up a New Web Service**:
   - Click "New" > "Web Service" in the Render dashboard.
   - Connect your GitHub repository containing the Movie Mood Ring project.

3. **Configure the Service**:
   - **Runtime**: Python.
   - **Build Command**: `pip install -r requirements.txt`.
   - **Start Command**: `gunicorn app:app`.
   - **Environment Variables**:
     - Add `TMDB_API_KEY` with your TMDb API key as the value.

4. **Deploy**:
   - Click "Create Web Service" to build and deploy.
   - Once deployed, access your app at the provided URL (e.g., `https://movie-mood-ring.onrender.com`).

## Running Tests
To ensure the app works as expected, run the provided tests:

1. **Install Testing Dependencies**:
   ```bash
   pip install pytest responses
   ```

2. **Run Tests**:
   From the project root, execute:
   ```bash
   pytest
   ```
   The tests cover key functionality like mood selection, recommendations, and the quiz.

## Usage
- **Select a Mood**: Choose a mood from the dropdown (e.g., "Happy" or "Spooky Halloween") and submit to get movie recommendations.
- **Take the Quiz**: Answer a few questions to discover your mood if you're unsure.
- **Explore Results**: View movie titles, posters, overviews, fun facts (taglines), and trailer links.
- **Try "Surprise Me!"**: Get random recommendations for a spontaneous movie night.

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request on GitHub.

Please report issues or suggest features via the [GitHub Issues](https://github.com/your-username/movie-mood-ring/issues) page.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy movie watching! 🍿 Let the Movie Mood Ring guide your next cinematic adventure!