import numpy as np
import pandas as pd

indices = pd.read_pickle('inputs/indices.pkl')
cosine_sim = pd.read_pickle('inputs/cosine_sim.pkl')
cosine_sim = cosine_sim.to_numpy()
titles = pd.read_pickle('inputs/titles.pkl')

def genre_recommendations(title):
    indices = pd.read_pickle('inputs/indices.pkl')
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]