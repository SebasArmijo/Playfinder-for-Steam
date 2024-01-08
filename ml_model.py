import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


path_items = './data/processed/df_items_clean.parquet'
path_genres = './data/processed/df_genres_dummies.parquet'
path_games = './data/processed/df_games_clean.parquet'
path_reviews = './data/processed/df_reviews_clean.parquet'


df_items = pd.read_parquet(path_items)
df_genres = pd.read_parquet(path_genres)
df_games = pd.read_parquet(path_games)
df_reviews = pd.read_parquet(path_reviews)

df_items['game_id'] = df_items['game_id'].astype(str)
df_genres['game_id'] = df_genres['game_id'].astype(str)
df_games['game_id'] = df_games['game_id'].astype(str)
df_reviews['game_id'] = df_reviews['game_id'].astype(str)
  
df_merged = df_games.merge(df_genres, on='game_id', how='left')

features = ['release_year'] + list(df_genres.columns[1:])  

scaler = StandardScaler()
df_merged['release_year'] = scaler.fit_transform(df_merged[['release_year']])

df_final = df_merged[['game_id'] + features]
df_final= df_final.merge(df_games[['game_id', 'app_name']], on='game_id', how='left')


df_sampled = df_final.sample(frac=0.5, random_state=42)

similarity_matrix = cosine_similarity(df_sampled[features].fillna(0))
similarity_matrix = np.nan_to_num(similarity_matrix)

def recomend_game_sampled(game_id, top_n=5):
    # Check if the game_id exists in the 'game_id' column of the sampled dataset
    if game_id not in df_sampled['game_id'].values:
        return f"No recommendations found: {game_id} is not in the sampled data." 

    # Find the game index in the sampled dataset
    game_idx = df_sampled.index[df_sampled['game_id'] == game_id].tolist()

    if not game_idx:
        return f"No recommendations found: Game with ID {game_id} not found in sampled data."

    game_idx = game_idx[0]  # Take the first index if multiple found

    # Similarity scores and sorting
    similarity_scores = list(enumerate(similarity_matrix[game_idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get top_n similar games
    similar_games_indices = [i for i, score in similarity_scores[1:top_n+1]]
    similar_game_names = df_sampled['app_name'].iloc[similar_games_indices].tolist()

    # Create the recommendation message
    recommendation_message = f"Recommended games based on game ID {game_id} - {df_sampled['app_name'].iloc[game_idx]}:"
    
    return [recommendation_message] + similar_game_names
