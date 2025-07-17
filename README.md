# 🎬 Movie Recommendation System

A Streamlit-based movie recommendation system that uses both content-based and collaborative filtering algorithms.

## Features

- **Interactive Rating System**: Rate movies with a 1-5 star system
- **Content-Based Filtering**: Get recommendations based on your favorite genres
- **Collaborative Filtering**: Discover movies based on your rating patterns
- **Responsive Design**: Works on desktop and mobile devices
- **CSV Data Storage**: Movies and ratings stored in CSV files
- **HTML Templates**: Customizable UI components

## Installation

1. Clone or download this repository
2. Install required packages:
      pip install -r requirements.txt
   ## Usage

1. Run the Streamlit app:
      streamlit run app.py
   2. Open your browser and navigate to `http://localhost:8501`

3. Start rating movies and get personalized recommendations!

## Project Structure

- `app.py`: Main Streamlit application
- `data/`: CSV files containing movie data and user ratings
- `templates/`: HTML templates for custom styling
- `utils/`: Python modules for data handling and recommendation algorithms

## How It Works

### Content-Based Filtering
Recommends movies based on genre preferences. It calculates similarity scores based on genre overlap and movie ratings.

### Collaborative Filtering
Analyzes your movie ratings to understand preferences, then recommends movies from genres you've rated highly.
