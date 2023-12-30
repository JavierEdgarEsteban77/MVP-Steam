import fastapi
import pandas as pd
import numpy as np
import uvicorn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

# Función para realizar análisis de sentimientos
def sentiment_analysis(review):
    """Realiza un análisis de sentimientos en una reseña.

    Args:
        review (str): La reseña a analizar.

    Returns:
        float: El puntaje de sentimiento de la reseña.
    """
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(review)
    return sentiment_scores['compound']

# Función para obtener el año de lanzamiento con más horas jugadas para un género específico
def PlayTimeGenre(genero: str):
    """Obtiene el año de lanzamiento con más horas jugadas para un género específico.

    Args:
        genero (str): El género de los juegos.

    Returns:
        dict: Un diccionario con el año de lanzamiento con más horas jugadas para el género dado.
    """
    df_genre = df_users_items_desanidado[df_users_items_desanidado['genero'] == genero]
    year_most_played = df_genre.groupby('año')['playtime_forever'].sum().idxmax()
    return {"Año de lanzamiento con más horas jugadas para Género X" : year_most_played}

# Función para obtener el usuario con más horas jugadas para un género específico
def UserForGenre(genero: str):
    """Obtiene el usuario con más horas jugadas para un género específico.

    Args:
        genero (str): El género de los juegos.

    Returns:
        dict: Un diccionario con el usuario que tiene más horas jugadas para el género dado y las horas jugadas por año.
    """
    df_genre = df_users_items_desanidado[df_users_items_desanidado['genero'] == genero]
    user_most_played = df_genre.groupby('user_id')['playtime_forever'].sum().idxmax()
    hours_played_per_year = df_genre[df_genre['user_id'] == user_most_played].groupby('año')['playtime_forever'].sum().to_dict()
    return {"Usuario con más horas jugadas para Género X" : user_most_played, "Horas jugadas": hours_played_per_year}

# Función para obtener los juegos más recomendados en un año específico
def UsersRecommend(año: int):
    """Obtiene los juegos más recomendados en un año específico.

    Args:
        año (int): El año de las recomendaciones.

    Returns:
        list: Una lista con los tres juegos más recomendados en el año dado.
    """
    df_year = df_user_reviews_desanidado[df_user_reviews_desanidado['año'] == año]
    df_recommended = df_year[df_year['recommend'] == True]
    top_games = df_recommended['item_name'].value_counts().nlargest(3).index.tolist()
    return [{"Puesto 1" : top_games[0]}, {"Puesto 2" : top_games[1]},{"Puesto 3" : top_games[2]}]

# Función para obtener los juegos menos recomendados en un año específico
def UsersNotRecommend(año: int):
    """Obtiene los juegos menos recomendados en un año específico.

    Args:
        año (int): El año de las recomendaciones.

    Returns:
        list: Una lista con los tres juegos menos recomendados en el año dado.
    """
    df_year = df_user_reviews_desanidado[df_user_reviews_desanidado['año'] == año]
    df_not_recommended = df_year[df_year['recommend'] == False]
    top_games = df_not_recommended['item_name'].value_counts().nlargest(3).index.tolist()
    return [{"Puesto 1" : top_games[0]}, {"Puesto 2" : top_games[1]},{"Puesto 3" : top_games[2]}]

# Función para obtener el análisis de sentimientos de las reseñas en un año específico
def sentiment_analysis_year(año: int):
    """Obtiene el análisis de sentimientos de las reseñas en un año específico.

    Args:
        año (int): El año de las reseñas.

    Returns:
        dict: Un diccionario con la cantidad de reseñas negativas, neutrales y positivas en el año dado.
    """
    df_year = df_user_reviews_desanidado[df_user_reviews_desanidado['año'] == año]
    sentiments = df_year['sentiment_analysis'].value_counts().to_dict()
    return sentiments

app = fastapi.FastAPI(title="MVP Steam PI ML OPs",
              description="Descripción: Obtener el Producto Mínimo Viable",
              contact={"name": "Javier Edgar Esteban",
                       "url": "https://github.com/JavierEdgarEsteban77/MVP-Steam",
                       "email": "javieredgaresteban@gmail.com",
                       "Tel.: +54 9 261 254 3003383"})

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
    uvicorn.run("mean:app", host="0.0.0.0", port=8000, reload=True)