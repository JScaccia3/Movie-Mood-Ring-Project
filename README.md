# final-project-implementation
This is the repository for my final project on movie recommendation web app

# The Movie Mood Ring

A web application that recommends movies based on your mood, powered by the TMDB API. Select a mood (Happy, Sad, Scary, Excited, or Surprise Me!) to receive a curated list of movie recommendations, including titles, posters, overviews, and fun facts.

## Features
- Choose a mood to get movie recommendations tailored to genres like Comedy, Drama, Horror, or Action.
- "Surprise Me!" option for random movie suggestions across all genres.
- Displays movie posters, overviews, and fun facts for an engaging user experience.
- Built with Flask and styled for a clean, intuitive interface.

## Installation

### Prerequisites
- [Anaconda](https://www.anaconda.com/products/distribution) for managing Python environments.
- A [TMDB API key](https://www.themoviedb.org/) for accessing movie data.
- Git installed [](https://git-scm.com/) to clone the repository.

### Steps
1. **Clone the Repository**:
   - Open a terminal:
     - **Mac**: Use Terminal (default shell is `zsh` or `bash`).
     - **Windows**: Use Command Prompt, PowerShell, or Git Bash (recommended, installed with Git).
   - Run:
     ```bash
     git clone https://github.com/your-username/movie-mood-ring.git
     cd movie-mood-ring

2. Set Up Anaconda Environment:

   - Install Anaconda if not already installed.
   - Create and activate a virtual environment:
     conda create -n movie_mood_ring python=3.9
     conda activate movie_mood_ring

3. Install Dependencies:
   - Install required Python packages:
     pip install -r requirements.txt

4. Set Up Environment Variables:

   - Create a .env file in the project root:
        - Mac: Use a text editor (e.g., VS Code, nano):
          echo "TMDB_API_KEY=your_api_key_here" > .env
        - Windows: Create .env in a text editor or use:
          echo TMDB_API_KEY=your_api_key_here > .env
   - Replace your_api_key_here with your TMDB API key from themoviedb.org.

5. Run the Application:
  
   - Start the Flask server:
     python app.py
   - Open your browser and navigate to http://localhost:5000.  