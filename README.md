# Movie Recommendation System

A Flask web application that provides content-based movie recommendations. Users can input a movie title and receive a list of similar movies based on pre-computed cosine similarity scores.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Customization](#customization)

## Overview

This application implements a content-based filtering recommendation system. It analyzes movie features (genres, keywords, cast, crew, etc.) to find movies similar to a user's input.

**Key Features:**
- Simple web interface for movie recommendations
- Pre-computed similarity matrix for fast lookups
- Adjustable number of recommendations
- Content-based filtering (no user data required)

## Installation

### Prerequisites
- Python 3.8+
- Flask
- pandas, numpy

### Setup

1. Navigate to the project directory:
```bash
cd app-classifier-movie-recommendation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure the required data files exist in the `inputs/` directory:
   - `indices.pkl` - Mapping of movie titles to indices
   - `cosine_sim.pkl` - Pre-computed cosine similarity matrix
   - `titles.pkl` - DataFrame of movie titles

## Usage

### Starting the Application

Run the Flask development server:
```bash
python app.py
```

The app will start on `http://localhost:5000`.

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Enter a movie title (e.g., "The Dark Knight")
3. Specify how many recommendations you want (default: 10)
4. Click submit to see similar movies

### Example

**Input:**
- Movie: "Inception"
- Number of recommendations: 5

**Output:**
```
1. Interstellar
2. The Prestige
3. Shutter Island
4. The Matrix
5. Memento
```

## How It Works

### Content-Based Filtering

The recommendation system works in two phases:

#### Phase 1: Pre-processing (Done Offline)
1. **Feature Extraction**: Extract movie features (genres, keywords, cast, crew, plot)
2. **Vectorization**: Convert features into numerical vectors (typically TF-IDF)
3. **Similarity Calculation**: Compute cosine similarity between all movie pairs
4. **Serialization**: Save matrices as pickle files for fast loading

#### Phase 2: Recommendation (Runtime)
1. User enters a movie title
2. System looks up the movie's index
3. Retrieves similarity scores for that movie
4. Sorts movies by similarity (descending)
5. Returns top N recommendations

### Cosine Similarity

The system uses cosine similarity to measure how similar two movies are:

```
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
```

- Values range from 0 (completely different) to 1 (identical)
- Focuses on feature overlap, not magnitude

### Why Content-Based?

**Advantages:**
- No cold start problem (works for new users immediately)
- Transparent recommendations (based on movie features)
- No user data required (privacy-friendly)

**Limitations:**
- Limited diversity (recommends similar movies)
- Requires good feature engineering
- Doesn't learn from user behavior

## Project Structure

```
app-classifier-movie-recommendation/
├── app.py                  # Flask application and routes
├── functions.py            # Recommendation logic
├── inputs/                 # Pre-computed model files
│   ├── indices.pkl         # Movie title → index mapping
│   ├── cosine_sim.pkl      # Similarity matrix
│   └── titles.pkl          # Movie titles dataframe
├── static/                 # CSS, JavaScript, images
│   ├── css/
│   └── js/
├── templates/              # HTML templates
│   ├── index.html          # Home page
│   └── post_movies.html    # Results page
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Customization

### Changing the Number of Recommendations

Edit `functions.py`:
```python
def genre_recommendations(title: str, top_n: int = 20):
    # Change top_n default value
```

### Modifying the UI

Edit templates in the `templates/` directory:
- `index.html` - Input form
- `post_movies.html` - Results display

### Adding More Features

To improve recommendations, regenerate the similarity matrix with additional features:

```python
# Example: Add director and year to features
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Combine features
df['combined_features'] = (
    df['genres'] + ' ' + 
    df['keywords'] + ' ' + 
    df['cast'] + ' ' + 
    df['director'] + ' ' +
    df['year'].astype(str)
)

# Vectorize
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Compute similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
```

## API Usage (Optional)

While this app uses HTML forms, you can also query it programmatically:

```python
import requests

url = "http://localhost:5000/post_movies"
data = {
    'movieChoice': 'The Matrix',
    'listSize': '10'
}

response = requests.post(url, data=data)
print(response.text)  # HTML response
```

## Troubleshooting

**"Movie not found" error:**
- Check spelling (titles are case-sensitive)
- Verify the movie exists in `inputs/titles.pkl`
- Try searching with the full official title

**Slow performance:**
- The similarity matrix is loaded into memory on startup
- For large datasets, consider using approximate nearest neighbors (ANN)

**Empty recommendations:**
- Ensure pickle files are not corrupted
- Verify cosine_sim.pkl contains valid similarity scores

## Future Enhancements

Potential improvements:
- Add autocomplete for movie titles
- Display movie posters with recommendations
- Implement hybrid filtering (content + collaborative)
- Add movie ratings and release years
- Cache frequently accessed recommendations

## Dependencies

```
Flask>=2.3.0
pandas>=2.0.0
numpy>=1.24.0
```

## License

This project is provided for educational and personal use.

