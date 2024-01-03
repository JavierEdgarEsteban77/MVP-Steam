# Importo librerías.
import fastapi
import pandas as pd
import numpy as np
import uvicorn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

# Carga los dataframes desde los archivos CSV.
df_users_items = pd.read_csv('C:\\Users\\Esteban García\\OneDrive\\Escritorio\\MVP Steam\\Data\\users_items.csv')
df_user_reviews = pd.read_csv('C:\\Users\\Esteban García\\OneDrive\\Escritorio\\MVP Steam\\Data\\user_reviews.csv')

# Función para realizar análisis de sentimientos
def sentiment_analysis(review):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(review)
    return sentiment_scores['compound']

# Función para obtener el año de lanzamiento con más horas jugadas para un género específico
def PlayTimeGenre(genero: str):
    df_genre = df_users_items[df_users_items['genero'] == genero]
    year_most_played = df_genre.groupby('año')['playtime_forever'].sum().idxmax()
    return {"Año de lanzamiento con más horas jugadas para Género X" : year_most_played}

# Función para obtener el usuario con más horas jugadas para un género específico
def UserForGenre(genero: str):
    df_genre = df_users_items[df_users_items['genero'] == genero]
    user_most_played = df_genre.groupby('user_id')['playtime_forever'].sum().idxmax()
    hours_played_per_year = df_genre[df_genre['user_id'] == user_most_played].groupby('año')['playtime_forever'].sum().to_dict()
    return {"Usuario con más horas jugadas para Género X" : user_most_played, "Horas jugadas": hours_played_per_year}

# Función para obtener los juegos más recomendados en un año específico
def UsersRecommend(año: int):
    df_year = df_user_reviews[df_user_reviews['año'] == año]
    df_recommended = df_year[df_year['recommend'] == True]
    top_games = df_recommended['item_name'].value_counts().nlargest(3).index.tolist()
    return [{"Puesto 1" : top_games[0]}, {"Puesto 2" : top_games[1]},{"Puesto 3" : top_games[2]}]

# Función para obtener los juegos menos recomendados en un año específico
def UsersNotRecommend(año: int):
    df_year = df_user_reviews[df_user_reviews['año'] == año]
    df_not_recommended = df_year[df_year['recommend'] == False]
    top_games = df_not_recommended['item_name'].value_counts().nlargest(3).index.tolist()
    return [{"Puesto 1" : top_games[0]}, {"Puesto 2" : top_games[1]},{"Puesto 3" : top_games[2]}]

# Función para obtener el análisis de sentimientos de las reseñas en un año específico
def sentiment_analysis_year(año: int):
    df_year = df_user_reviews[df_user_reviews['año'] == año]
    sentiments = df_year['sentiment_analysis'].value_counts().to_dict()
    return sentiments

app = fastapi.FastAPI(title="MVP Steam PI ML OPs")

@app.get("/PlayTimeGenre/{genero}")
def get_PlayTimeGenre(genero: str):
    return PlayTimeGenre(genero)

@app.get("/UserForGenre/{genero}")
def get_UserForGenre(genero: str):
    return UserForGenre(genero)

@app.get("/UsersRecommend/{año}")
def get_UsersRecommend(año: int):
    return UsersRecommend(año)

@app.get("/UsersNotRecommend/{año}")
def get_UsersNotRecommend(año: int):
    return UsersNotRecommend(año)

@app.get("/sentiment_analysis_year/{año}")
def get_sentiment_analysis_year(año: int):
    return sentiment_analysis_year(año)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
