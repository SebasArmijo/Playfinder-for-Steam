from fastapi import FastAPI
import pandas as pd
from ml_model import recommend_game 

app = FastAPI()

def playtime_genre(genre: str):
    df_combined = pd.read_parquet('./data/processed/playtime_genre_combined.parquet')
    genre_lower = genre.lower()

    # Find the corresponding column for the genre
    genre_column = next((col for col in df_combined.columns if col.lower() == genre_lower), None)

    if not genre_column:
        return {"error": f"Genre '{genre}' not found"}
    genre_df = df_combined[df_combined[genre_column] == 1]
    playtime_by_year = genre_df.groupby('release_year')['playtime_forever'].sum()
    max_playtime_year = playtime_by_year.idxmax()
    return {"Year with most hours played for Genre {}".format(genre): int(max_playtime_year)}

def user_for_genre(genre: str):
    # Load the combined dataset
    df_combined = pd.read_parquet('./data/processed/user_genre_combined.parquet')

    genre_lower = genre.lower()
    genre_column = next((col for col in df_combined.columns if col.lower() == genre_lower), None)
    if not genre_column:
        return {"error": f"Genre '{genre}' not found"}
    genre_df = df_combined[df_combined[genre_column] == 1]
    user_playtime = genre_df.groupby('user_id')['playtime_forever'].sum()
    top_user = user_playtime.idxmax()
    playtime_by_year = genre_df[genre_df['user_id'] == top_user].groupby('release_year')['playtime_forever'].sum().reset_index()
    playtime_by_year = playtime_by_year[playtime_by_year['playtime_forever'] > 0]
    playtime_by_year = playtime_by_year.sort_values('release_year', ascending=False)

    return {
        "User with most hours played for Genre {}".format(genre): str(top_user),
        "Hours Played": playtime_by_year.to_dict(orient='records')
    }

def users_recommend(year: int):
    df_combined_reviews = pd.read_parquet('./data/processed/games_reviews_combined.parquet')
    year_games = df_combined_reviews[df_combined_reviews['release_year'] == year]
    if year_games.empty:
        return {"message": f"No data available for the year {year}"}
    recommended_reviews = year_games[year_games['recommend'] == True]
    top_games = recommended_reviews['app_name'].value_counts().head(3).index.tolist()
    top_games_ranked = [{"Rank {}".format(i + 1): game} for i, game in enumerate(top_games)]
    if not top_games_ranked:
        return {"message": f"No recommended games found for the year {year}"}

    return {"Top recommended games for the year {}".format(year): top_games_ranked}


def users_worst_developer(year: int):
    df_combined_reviews_developer = pd.read_parquet('./data/processed/games_reviews_developer_combined.parquet')
    year_games = df_combined_reviews_developer[df_combined_reviews_developer['release_year'] == year]
    if year_games.empty:
        return {"message": f"No data available for the year {year}"}
    negative_reviews = year_games[year_games['recommend'] == False]
    worst_developers = negative_reviews['developer'].value_counts().nsmallest(3).index.tolist()
    worst_developers_ranked = [{"Rank {}".format(i + 1): dev} for i, dev in enumerate(worst_developers)]

    if not worst_developers_ranked:
        return {"message": f"No negative reviews found for developers in the year {year}"}

    return {"Top 3 developers with the most negative reviews for the year {}".format(year): worst_developers_ranked}


def sentiment_analysis(developer: str):
    df_combined_sentiment = pd.read_parquet('./data/processed/games_sentiment_combined.parquet')
    developer_lower = developer.lower()
    matched_developer = df_combined_sentiment['developer'].str.lower().eq(developer_lower)
    if not matched_developer.any():
        return {"error": f"Developer '{developer}' not found"}
    dev_reviews = df_combined_sentiment[matched_developer]
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
def game_recommendations(game_id: int):  # Changed type to int
    try:
        recommendations = recommend_game(game_id)  # Ensure this is the correct function name
        return {"recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}