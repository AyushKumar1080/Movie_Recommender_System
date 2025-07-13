import pandas as pd
import os

class DataHandler:
    def __init__(self):
        self.data_path = "data"
        
    def load_movies(self):
        """Load movies from CSV file"""
        movies_path = os.path.join(self.data_path, "movies.csv")
        if os.path.exists(movies_path):
            df = pd.read_csv(movies_path)
            return df
        else:
            # Return empty DataFrame if file doesn't exist
            return pd.DataFrame(columns=['id', 'title', 'genres', 'year', 'director', 'rating'])
    
    def load_user_ratings(self):
        """Load user ratings from CSV file"""
        ratings_path = os.path.join(self.data_path, "user_ratings.csv")
        if os.path.exists(ratings_path):
            df = pd.read_csv(ratings_path)
            return df
        else:
            return pd.DataFrame(columns=['user_id', 'movie_id', 'rating', 'timestamp'])
    
    def save_user_rating(self, user_id, movie_id, rating):
        """Save a user rating to CSV file"""
        ratings_df = self.load_user_ratings()
        new_rating = pd.DataFrame({
            'user_id': [user_id],
            'movie_id': [movie_id],
            'rating': [rating],
            'timestamp': [pd.Timestamp.now()]
        })
        
        # Remove existing rating for this user-movie pair
        ratings_df = ratings_df[~((ratings_df['user_id'] == user_id) & 
                                 (ratings_df['movie_id'] == movie_id))]
        
        # Add new rating
        ratings_df = pd.concat([ratings_df, new_rating], ignore_index=True)
        
        # Save to CSV
        ratings_path = os.path.join(self.data_path, "user_ratings.csv")
        ratings_df.to_csv(ratings_path, index=False)
    
    def get_all_genres(self):
        """Get all unique genres from movies"""
        movies_df = self.load_movies()
        all_genres = set()
        
        for genres_str in movies_df['genres']:
            if pd.notna(genres_str):
                genres = [genre.strip() for genre in genres_str.split(',')]
                all_genres.update(genres)
        
        return sorted(list(all_genres))
    
    def get_movies_by_genre(self, selected_genres):
        """Get movies that match selected genres"""
        movies_df = self.load_movies()
        matching_movies = []
        
        for _, movie in movies_df.iterrows():
            if pd.notna(movie['genres']):
                movie_genres = [genre.strip() for genre in movie['genres'].split(',')]
                if any(genre in selected_genres for genre in movie_genres):
                    matching_movies.append(movie)
        
        return pd.DataFrame(matching_movies)