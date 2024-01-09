import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def recommend_game(game_id, top_n=5):
    df_sampled = pd.read_parquet('./data/processed/preprocessed_sample_for_recommendation.parquet')
    df_sampled = df_sampled.reset_index(drop=True)

    numeric_features = df_sampled.select_dtypes(include=[np.number]).columns.tolist()
    similarity_matrix = cosine_similarity(df_sampled[numeric_features].fillna(0))
    similarity_matrix = np.nan_to_num(similarity_matrix)

    if game_id not in df_sampled['game_id'].values:
        return f"No recommendations found: {game_id} is not in the data."

    game_idx = df_sampled.index[df_sampled['game_id'] == game_id].tolist()
    if not game_idx:
        return f"No recommendations found: Game with ID {game_id} not found in data."
    game_idx = game_idx[0]

    similarity_scores = list(enumerate(similarity_matrix[game_idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    similar_games_indices = [i for i, score in similarity_scores[1:top_n+1]]
    similar_game_names = df_sampled['app_name'].iloc[similar_games_indices].tolist()

    input_game_name = df_sampled['app_name'].iloc[game_idx]
    recommendation_message = f"Recommended games based on game ID {game_id} - {input_game_name}:"
    
    return [recommendation_message] + similar_game_names

