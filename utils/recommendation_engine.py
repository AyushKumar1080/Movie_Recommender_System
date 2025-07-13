import pandas as pd
import numpy as np
from collections import defaultdict

class RecommendationEngine:
    def __init__(self, movies_df):
        self.movies_df = movies_df
    
    def content_based_recommendations(self, selected_genres, top_n=6):
        """Generate content-based recommendations based on selected genres"""
        if not selected_genres:
            return pd.DataFrame()
        
        scored_movies = []
        
        for _, movie in self.movies_df.iterrows():
            if pd.notna(movie['genres']):
                movie_genres = [genre.strip() for genre in movie['genres'].split(',')]
                
                # Calculate genre overlap
                genre_overlap = len(set(movie_genres) & set(selected_genres))
                
                if genre_overlap > 0:
                    # Score based on genre overlap and movie rating
                    score = (genre_overlap / len(selected_genres)) * movie['rating']
                    scored_movies.append({
                        'movie': movie,
                        'score': score
                    })
        
        # Sort by score and return top N
        scored_movies.sort(key=lambda x: x['score'], reverse=True)
        top_movies = [item['movie'] for item in scored_movies[:top_n]]
        
        return pd.DataFrame(top_movies)
    
    def collaborative_filtering(self, user_ratings, top_n=6):
        """Generate collaborative filtering recommendations based on user ratings"""
        if len(user_ratings) < 2:
            return pd.DataFrame()
        
        # Calculate genre preferences based on ratings
        genre_preferences = defaultdict(float)
        
        for movie_id, rating in user_ratings.items():
            if rating >= 4:  # Only consider highly rated movies
                movie = self.movies_df[self.movies_df['id'] == movie_id]
                if not movie.empty and pd.notna(movie.iloc[0]['genres']):
                    movie_genres = [genre.strip() for genre in movie.iloc[0]['genres'].split(',')]
                    for genre in movie_genres:
                        genre_preferences[genre] += rating
        
        # Score unrated movies based on genre preferences
        rated_movie_ids = set(user_ratings.keys())
        scored_movies = []
        
        for _, movie in self.movies_df.iterrows():
            if movie['id'] not in rated_movie_ids and pd.notna(movie['genres']):
                movie_genres = [genre.strip() for genre in movie['genres'].split(',')]
                
                # Calculate score based on genre preferences
                score = 0
                for genre in movie_genres:
                    score += genre_preferences.get(genre, 0)
                
                # Weight by movie rating
                final_score = score * (movie['rating'] / 10)
                
                if final_score > 0:
                    scored_movies.append({
                        'movie': movie,
                        'score': final_score
                    })
        
        # Sort by score and return top N
        scored_movies.sort(key=lambda x: x['score'], reverse=True)
        top_movies = [item['movie'] for item in scored_movies[:top_n]]
        
        return pd.DataFrame(top_movies)
    
    def hybrid_recommendations(self, user_ratings, selected_genres, top_n=6):
        """Combine content-based and collaborative filtering"""
        content_recs = self.content_based_recommendations(selected_genres, top_n * 2)
        collab_recs = self.collaborative_filtering(user_ratings, top_n * 2)
        
        # Combine and deduplicate
        all_recs = pd.concat([content_recs, collab_recs]).drop_duplicates(subset=['id'])
        
        return all_recs.head(top_n)