import fastapi
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')


def sentiment_analysis(review):
    # Instancia el analizador de sentimientos
    sid = SentimentIntensityAnalyzer()

    # Calcula los puntajes de sentimiento para la reseña
    sentiment_scores = sid.polarity_scores(review)

    # Devuelve el puntaje de sentimiento compuesto
    return sentiment_scores['compound']


def recomendacion_juego(item_id: int, generos_favoritos: List[str] = None):
    # Encuentro el juego con el item_id dado.
    game_index = df_steam_games[df_steam_games['item_id'] == item_id].index[0]

    # Encuentro los 100 juegos más similares.
    similar_games = []
    for i in range(len(df_steam_games)):
        if i != game_index:
            if generos_favoritos:
                if set(df_steam_games.iloc[i]['genero']).intersection(generos_favoritos):
                    similar_games.append((i, cosine_sim[i]))
            else:
                similar_games.append((i, cosine_sim[i]))

    # Ordeno la lista de juegos similares por similitud.
    similar_games.sort(key=lambda x: x[1], reverse=True)

    # Devuelve los juegos recomendados
    recommended_games = [
        {
            'app_name': game['app_name'],
            'genero': game['genero'],
            'plataforma': game['plataforma'],
            'puntuacion': game['puntuacion'],
        }
        for i, game in similar_games[:100]
    ]

    # Encuentro las reseñas de los usuarios para el juego dado.
    reviews = df_user_reviews_desanidado[df_user_reviews_desanidado['item_id'] == item_id]

    # Encuentro las reseñas más votadas.
    top_reviews = reviews.sort_values(by='helpful', ascending=False).head(3)

    # Analizo el sentimiento de las reseñas.
    review_sentiment = []
    for review in top_reviews['reviews']:
        review_sentiment.append(sentiment_analysis(review))

    # Devuelve los juegos recomendados y la información de las reseñas.
    return {
        'Juegos recomendados': recommended_games,
        'Reseñas': top_reviews,
        'Sentimiento de las reseñas': review_sentiment,
    }


def autenticar_usuario(username: str, password: str):
    # ...

    return True


app = fastapi.FastAPI()


@app.get("/recomendacion_juego/{item_id}")
def get_recomendacion_juego(item_id: int, username: str = None, password: str = None):
    # ...

    if username and password:
        if not autenticar_usuario(username, password):
            return {'error': 'Acceso denegado'}

    recommended_games = recomendacion_juego(item_id)

    # ...

    return recommended_games


if __name__ == '__main__':
    app.run(debug=True)