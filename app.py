import streamlit as st
import pandas as pd
import numpy as np
from utils.data_handler import DataHandler
from utils.recommendation_engine import RecommendationEngine
import os

# Page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom HTML templates
def load_html_template(template_name):
    template_path = os.path.join("templates", template_name)
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Initialize session state
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = {}
if 'selected_genres' not in st.session_state:
    st.session_state.selected_genres = []
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

# Initialize data handler and recommendation engine
@st.cache_data
def load_data():
    data_handler = DataHandler()
    return data_handler.load_movies(), data_handler.get_all_genres()

def main():
    # Load header template
    header_html = load_html_template("header.html")
    if header_html:
        st.markdown(header_html, unsafe_allow_html=True)
    
    # Load data
    movies_df, all_genres = load_data()
    rec_engine = RecommendationEngine(movies_df)
    
    # Main title
    st.title("🎬 Movie Recommendation System")
    st.markdown("### Discover your next favorite movie using AI-powered recommendations")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    tab_selection = st.sidebar.radio(
        "Choose Recommendation Method:",
        ["Rate Movies", "Genre-Based", "Collaborative Filtering"]
    )
    
    # Tab 1: Rate Movies
    if tab_selection == "Rate Movies":
        st.header("⭐ Rate Some Movies")
        st.markdown("Rate at least 2 movies to get collaborative recommendations")
        
        # Display movies for rating
        cols = st.columns(3)
        for idx, (_, movie) in enumerate(movies_df.head(12).iterrows()):
            with cols[idx % 3]:
                st.subheader(movie['title'])
                st.write(f"**{movie['year']}** • {movie['director']}")
                st.write(f"*{movie['genres']}*")
                
                # Star rating
                rating = st.select_slider(
                    f"Rate {movie['title']}:",
                    options=[0, 1, 2, 3, 4, 5],
                    value=st.session_state.user_ratings.get(movie['id'], 0),
                    key=f"rating_{movie['id']}"
                )
                
                if rating > 0:
                    st.session_state.user_ratings[movie['id']] = rating
                elif movie['id'] in st.session_state.user_ratings:
                    del st.session_state.user_ratings[movie['id']]
        
        # Display rating summary
        st.sidebar.markdown("### Your Ratings")
        st.sidebar.write(f"Movies Rated: {len(st.session_state.user_ratings)}")
        if st.session_state.user_ratings:
            avg_rating = np.mean(list(st.session_state.user_ratings.values()))
            st.sidebar.write(f"Average Rating: {avg_rating:.1f}")
    
    # Tab 2: Genre-Based Recommendations
    elif tab_selection == "Genre-Based":
        st.header("🎭 Content-Based Filtering")
        st.markdown("Select your favorite genres to get recommendations")
        
        # Genre selection
        st.subheader("Select Genres:")
        selected_genres = st.multiselect(
            "Choose your preferred genres:",
            all_genres,
            default=st.session_state.selected_genres
        )
        st.session_state.selected_genres = selected_genres
        
        if st.button("Get Genre-Based Recommendations", type="primary"):
            if selected_genres:
                with st.spinner("Generating recommendations..."):
                    recommendations = rec_engine.content_based_recommendations(selected_genres)
                    st.session_state.recommendations = recommendations
            else:
                st.warning("Please select at least one genre!")
    
    # Tab 3: Collaborative Filtering
    elif tab_selection == "Collaborative Filtering":
        st.header("👥 Collaborative Filtering")
        st.markdown("Based on your ratings, we'll find movies similar users enjoyed")
        
        # Rating summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Movies Rated", len(st.session_state.user_ratings))
        with col2:
            highly_rated = len([r for r in st.session_state.user_ratings.values() if r >= 4])
            st.metric("Highly Rated", highly_rated)
        with col3:
            if st.session_state.user_ratings:
                avg_rating = np.mean(list(st.session_state.user_ratings.values()))
                st.metric("Avg Rating", f"{avg_rating:.1f}")
            else:
                st.metric("Avg Rating", "0")
        with col4:
            to_discover = len(movies_df) - len(st.session_state.user_ratings)
            st.metric("To Discover", to_discover)
        
        if st.button("Get Collaborative Recommendations", type="primary"):
            if len(st.session_state.user_ratings) >= 2:
                with st.spinner("Analyzing your preferences..."):
                    recommendations = rec_engine.collaborative_filtering(st.session_state.user_ratings)
                    st.session_state.recommendations = recommendations
            else:
                st.warning("Please rate at least 2 movies in the 'Rate Movies' tab first!")
    
    # Display recommendations
    if st.session_state.recommendations:
        st.header("🎯 Recommended for You")
        
        # Load movie card template
        movie_card_template = load_html_template("movie_card.html")
        
        cols = st.columns(3)
        for idx, (_, movie) in enumerate(st.session_state.recommendations.head(6).iterrows()):
            with cols[idx % 3]:
                if movie_card_template:
                    # Use HTML template
                    card_html = movie_card_template.format(
                        title=movie['title'],
                        year=movie['year'],
                        director=movie['director'],
                        genres=movie['genres'],
                        rating=movie['rating'],
                        rank=idx + 1
                    )
                    st.markdown(card_html, unsafe_allow_html=True)
                else:
                    # Fallback to Streamlit components
                    st.subheader(f"#{idx + 1} {movie['title']}")
                    st.write(f"**{movie['year']}** • {movie['director']}")
                    st.write(f"*{movie['genres']}*")
                    st.write(f"⭐ {movie['rating']}")
    
    # Algorithm explanation
    with st.expander("🧠 How It Works"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Content-Based Filtering")
            st.write("""
            Recommends movies based on the genres you select. It calculates 
            similarity scores based on genre overlap and movie ratings to 
            suggest films you might enjoy.
            """)
        with col2:
            st.subheader("Collaborative Filtering")
            st.write("""
            Analyzes your movie ratings to understand your preferences, then 
            recommends movies from genres you've rated highly. It's like 
            getting suggestions from users with similar tastes.
            """)
    
    # Load footer template
    footer_html = load_html_template("footer.html")
    if footer_html:
        st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()