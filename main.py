from fastapi import FastAPI
import pandas as pd
from ml_model import recomend_game_sampled  


app = FastAPI()


# Function to load data
def load_data():
    path_items = './data/processed/df_items_clean.parquet'
    path_genres = './data/processed/df_genres_dummies.parquet'
    path_games = './data/processed/df_games_clean.parquet'
    path_reviews = './data/processed/df_reviews_clean.parquet'

    # Load the dataframes
    df_items = pd.read_parquet(path_items)
    df_genres = pd.read_parquet(path_genres)
    df_games = pd.read_parquet(path_games)
    df_reviews = pd.read_parquet(path_reviews)

    # Convert 'game_id' to Int64 in all dataframes where it exists
    if 'game_id' in df_items.columns:
        df_items['game_id'] = df_items['game_id'].astype('Int64')
    if 'game_id' in df_reviews.columns:
        df_reviews['game_id'] = df_reviews['game_id'].astype('Int64')
    if 'game_id' in df_genres.columns:
        df_genres['game_id'] = df_genres['game_id'].astype('Int64')
    if 'game_id' in df_games.columns:
        df_games['game_id'] = df_games['game_id'].astype('Int64')

    return df_items, df_reviews, df_genres, df_games

# Load data once when the server starts
df_items, df_reviews, df_genres, df_games = load_data()

def playtime_genre(genre: str):
    genre_lower = genre.lower()
    genre_column = next((col for col in df_genres.columns if col.lower() == genre_lower), None)
    
    if not genre_column:
        return {"error": f"Genre '{genre}' not found"}

    genre_df = df_genres[df_genres[genre_column] == 1]
    merged_df = pd.merge(df_items, df_games, on='game_id')
    merged_df = pd.merge(merged_df, genre_df, on='game_id')
    playtime_by_year = merged_df.groupby('release_year')['playtime_forever'].sum()
    max_playtime_year = playtime_by_year.idxmax()
    return {"Year with most hours played for Genre {}".format(genre): int(max_playtime_year)}

def user_for_genre(genre: str):
    genre_lower = genre.lower()
    genre_column = next((col for col in df_genres.columns if col.lower() == genre_lower), None)
    
    if not genre_column:
        return {"error": f"Genre '{genre}' not found"}

    genre_df = df_genres[df_genres[genre_column] == 1]
    merged_df = pd.merge(df_items, df_games, on='game_id')
    merged_df = pd.merge(merged_df, genre_df, on='game_id')
    user_playtime = merged_df.groupby('user_id')['playtime_forever'].sum()
    top_user = user_playtime.idxmax()

    playtime_by_year = merged_df[merged_df['user_id'] == top_user].groupby('release_year')['playtime_forever'].sum().reset_index()
    playtime_by_year = playtime_by_year[playtime_by_year['playtime_forever'] > 0]  
    playtime_by_year = playtime_by_year.sort_values('release_year', ascending=False)  

    return {
        "User with most hours played for Genre {}".format(genre): str(top_user),
        "Hours Played": playtime_by_year.to_dict(orient='records')
    }


def users_recommend(year: int):
    year_games = df_games[df_games['release_year'] == year]
    year_reviews = pd.merge(year_games, df_reviews, on='game_id')
    recommended_reviews = year_reviews[year_reviews['recommend'] == True]
    top_games = recommended_reviews['app_name'].value_counts().head(3).index.tolist()
    top_games_ranked = [{"Rank {}".format(i + 1): game} for i, game in enumerate(top_games)]

    return {"Top recommended games for the year {}".format(year): top_games_ranked}


def users_worst_developer(year: int):
    year_games = df_games[df_games['release_year'] == year]
    year_reviews = pd.merge(year_games, df_reviews, on='game_id')
    negative_reviews = year_reviews[year_reviews['recommend'] == False]
    worst_developers = negative_reviews['developer'].value_counts().nsmallest(3).index.tolist()
    worst_developers_ranked = [{"Rank {}".format(i + 1): dev} for i, dev in enumerate(worst_developers)]

    return {"Top 3 developers with the most negative reviews for the year {}".format(year): worst_developers_ranked}


def sentiment_analysis(developer: str):
    developer_lower = developer.lower()
    matched_developer = df_games['developer'].str.lower().eq(developer_lower)
    if not matched_developer.any():
        return {"error": f"Developer '{developer}' not found"}
    dev_games = df_games[matched_developer]
    dev_reviews = pd.merge(dev_games, df_reviews, on='game_id')
    if dev_reviews.empty:
        return {"message": "No reviews found for developer {}".format(developer)}
    sentiment_count = dev_reviews['sentiment_analysis'].value_counts().rename({0: 'Negative', 1: 'Neutral', 2: 'Positive'})

    return {"Sentiment analysis for developer {}".format(developer): sentiment_count.to_dict()}



# Endpoint definitions for FastAPI
@app.get("/PlayTimeGenre/{genre}")
def endpoint_playtime_genre(genre: str):
    return playtime_genre(genre)

@app.get("/UserForGenre/{genre}")
def endpoint_user_for_genre(genre: str):
    return user_for_genre(genre)

@app.get("/UsersRecommend/{year}")
def endpoint_users_recommend(year: int):
    return users_recommend(year)

@app.get("/UsersWorstDeveloper/{year}")
def endpoint_users_worst_developer(year: int):
    return users_worst_developer(year)

@app.get("/sentiment_analysis/{developer}")
def endpoint_sentiment_analysis(developer: str):
    return sentiment_analysis(developer)

@app.get("/game_recommendations/{game_id}")
def game_recommendations(game_id: str):
    recommendations = recomend_game_sampled(game_id)
    return {"recommendations": recommendations}






