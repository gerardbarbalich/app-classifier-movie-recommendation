"""
Movie Recommendation Flask Web Application.

This application provides a web interface for a content-based movie recommendation
system. Users can input a movie title and receive recommendations for similar movies
based on cosine similarity of movie features.
"""

from flask import Flask, render_template, request
import pandas as pd
from functions import genre_recommendations

# Initialize Flask application
app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    """
    Render the home page of the movie recommendation app.
    
    Returns:
        Rendered HTML template for the main page
    """
    title = 'Movie Recommendation System'
    return render_template('index.html', title=title)


@app.route('/post_movies', methods=['POST'])
def post_movies():
    """
    Handle POST request with movie choice and generate recommendations.
    
    This endpoint receives a form submission with:
    - movieChoice: The title of the movie to base recommendations on
    - listSize: Number of recommendations to return
    
    Returns:
        Rendered HTML template with recommendation results in a table
    """
    # Extract form inputs
    movie_choice = request.form.get('movieChoice')
    list_size = request.form.get('listSize')
    
    # Convert list size to integer
    try:
        list_size = int(list_size)
    except (ValueError, TypeError):
        # Default to 10 if invalid input
        list_size = 10
    
    # Generate recommendations using content-based filtering
    series = genre_recommendations(movie_choice).head(list_size)
    df = pd.DataFrame(series)

    # Render results as an HTML table
    return render_template(
        'post_movies.html', 
        names=[df.to_html(classes='data', index=False)], 
        titles=df.columns.values
    )


if __name__ == '__main__':
    # Run the Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)
