"""
Movie recommendation functions using content-based filtering.

This module implements a content-based recommendation system that suggests
movies similar to a given movie based on cosine similarity of features
(likely genres, keywords, cast, etc.).
"""

import numpy as np
import pandas as pd
from typing import Optional

# Load pre-computed data files
# These are generated during the model training phase
indices = pd.read_pickle('inputs/indices.pkl')      # Maps movie titles to indices
cosine_sim = pd.read_pickle('inputs/cosine_sim.pkl')  # Similarity matrix
cosine_sim = cosine_sim.to_numpy()                  # Convert to numpy for faster lookup
titles = pd.read_pickle('inputs/titles.pkl')        # DataFrame of movie titles


def genre_recommendations(title: str, top_n: int = 20) -> pd.Series:
    """
    Generate movie recommendations based on content similarity.
    
    This function uses pre-computed cosine similarity scores to find movies
    that are most similar to the input movie. The similarity is based on
    movie features such as genre, keywords, cast, and crew.
    
    Args:
        title: The title of the movie to base recommendations on
        top_n: Maximum number of recommendations to return (default: 20)
    
    Returns:
        pd.Series: Series of recommended movie titles, ordered by similarity
    
    Raises:
        KeyError: If the movie title is not found in the dataset
    
    Example:
        >>> recommendations = genre_recommendations('The Dark Knight')
        >>> print(recommendations.head())
    """
    # Reload indices to ensure we have the latest data
    # Note: This is redundant with global loading but kept for consistency
    indices_local = pd.read_pickle('inputs/indices.pkl')
    
    try:
        # Get the index of the movie that matches the title
        idx = indices_local[title]
    except KeyError:
        raise KeyError(f"Movie '{title}' not found in database. Please check the spelling.")
    
    # Get pairwise similarity scores for this movie with all movies
    # Returns list of tuples: [(movie_index, similarity_score), ...]
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort movies by similarity score (descending order)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top N most similar movies (excluding the first one, which is itself)
    sim_scores = sim_scores[1:top_n+1]
    
    # Extract movie indices from the tuples
    movie_indices = [i[0] for i in sim_scores]
    
    # Return the titles of the most similar movies
    return titles.iloc[movie_indices]


def get_all_movie_titles() -> pd.Series:
    """
    Retrieve the complete list of available movie titles.
    
    Returns:
        pd.Series: All movie titles in the database
    """
    return titles


def check_movie_exists(title: str) -> bool:
    """
    Check if a movie title exists in the database.
    
    Args:
        title: Movie title to check
    
    Returns:
        bool: True if movie exists, False otherwise
    """
    return title in indices.index