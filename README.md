# Movie Mood Ring

The Movie Mood Ring is a Flask web application that recommends movies based on your current mood. It uses the [TMDB API](https://www.themoviedb.org/) to fetch movie data and provides a fun, interactive way to discover new films.

## Setup (Local)

To run this app locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/movie-mood-ring.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd movie-mood-ring
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
4. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
6. **Set the TMDB API key as an environment variable**:
   - On macOS/Linux:
     ```bash
     export TMDB_API_KEY=your_api_key_here
     ```
   - On Windows:
     ```bash
     set TMDB_API_KEY=your_api_key_here
     ```
7. **Run the app**:
   ```bash
   flask run
   ```
8. **Access the app**:
   - Open your browser and navigate to `http://127.0.0.1:5000`.

## Deployment on Render.com

To deploy this app on Render.com, follow these steps:

1. **Sign up for a Render account**:
   - Go to [Render.com](https://render.com/) and create an account.

2. **Create a new web service**:
   - From the Render dashboard, click "New" and select "Web Service."
   - Connect your GitHub repository by selecting it or entering the repository URL.

3. **Configure the web service**:
   - **Build Command**: Leave as default (`pip install -r requirements.txt`).
   - **Start Command**: Set to `gunicorn app:app` (ensure your Flask app is named `app` in `app.py`).
   - **Environment Variables**: Add `TMDB_API_KEY` with your TMDB API key as the value.

4. **Deploy the app**:
   - Click "Create Web Service" to initiate deployment.
   - Once complete, Render provides a URL (e.g., `https://your-app-name.onrender.com`) to access your live app.

## Usage

- Select a mood from the dropdown menu and click "Get Recommendations" to see movie suggestions.
- Use the mood quiz if you're unsure about your current mood.
- Enjoy discovering new movies!

## Notes

- **TMDB API Key**: Obtain a key by signing up on the [TMDB website](https://www.themoviedb.org/).
- **Requirements**: Ensure `requirements.txt` includes `Flask`, `requests`, `python-dotenv`, and `gunicorn`.
- **Issues**: Report problems or suggestions by opening an issue on the GitHub repository.