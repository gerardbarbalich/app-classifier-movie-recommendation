from flask import Flask, render_template, request, url_for, jsonify
import pandas as pd
from functions import genre_recommendations

app = Flask(__name__)
app.debug=True

@app.route('/')
def hello_world():
    title = 'Our website'
    return render_template('index.html', title=title)

@app.route('/post_movies', methods=['POST'])
def post_movies():
    
    # gather inputs
    movie_choice = request.form.get('movieChoice')
    list_size = request.form.get('listSize')
    list_size = int(list_size)

    # run recommendations
    series = genre_recommendations(movie_choice).head(list_size)
    df = pd.DataFrame(series)

    return render_template('post_movies.html', names=[df.to_html(classes='data')], titles=df.columns.values)
