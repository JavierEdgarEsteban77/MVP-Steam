# Importo las librerías y recursos necesarios.
import fastapi
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

# Defino la función de análisis de sentimientos.
def sentiment_analysis(review):
    # Instancia el analizador de sentimientos
    sid = SentimentIntensityAnalyzer()

    # Calcula los puntajes de sentimiento para la reseña
    sentiment_scores = sid.polarity_scores(review)

    # Devuelve el puntaje de sentimiento compuesto
    return sentiment_scores['compound']

# Leo los datos.
df_steam_games = pd.read_csv('steam_games.csv')
df_user_reviews_desanidado = pd.read_csv('user_reviews.csv')
df_users_items_desanidado = pd.read_csv('users_items.csv')

# Creo una nueva columna que combina 'app_name' con tus columnas de géneros.
df_steam_games['combined'] = df_steam_games['app_name'] + ' ' + df_steam_games['Action'].astype(str) + ' ' + df_steam_games['Adventure'].astype(str) + ' ' + df_steam_games['Animation & Modeling'].astype(str) + ' ' + df_steam_games['Audio Production'].astype(str) + ' ' + df_steam_games['Casual'].astype(str) + ' ' + df_steam_games['Design & Illustration'].astype(str) + ' ' + df_steam_games['Early Access'].astype(str) + ' ' + df_steam_games['Education'].astype(str) + ' ' + df_steam_games['Free to Play'].astype(str) + ' ' + df_steam_games['Indie'].astype(str) + ' ' + df_steam_games['Massively Multiplayer'].astype(str)

# Creo la matriz de características utilizando la columna 'combined'.
count = CountVectorizer(stop_words='english', ngram_range=(1, 2))
count_matrix = count.fit_transform(df_steam_games['combined'])

# Calculo la similitud del coseno.
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Defino la función.
def recomendacion_juego(item_id: int):
    # Encuentro el juego con el item_id dado.
    game_index = df_steam_games[df_steam_games['item_id'] == item_id].index[0]

    # Encuentro los 100 juegos más similares.
    similar_games = []
    for i in range(len(df_steam_games)):
        if i != game_index:
            similar_games.append((i, cosine_sim[i]))

    # Ordeno la lista de juegos similares por similitud.
    similar_games.sort(key=lambda x: x[1], reverse=True)

    # Devuelve los juegos recomendados
    recommended_games = [df_steam_games.iloc[i[0]]['app_name'] for i in similar_games[:100]]

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
        'Sentimiento de las reseñas': review_sentiment
    }

# Creo la aplicación.
app = FastAPI()

# Defino los endpoints.
@app.get("/recomendacion_juego/{item_id}")
def recomendacion_juego(item_id: int):
    recommended_games = recomendacion_juego(item_id)

    # Renderizo los resultados en formato JSON.
    return jsonify(recommended_games)

# Inicia la aplicación.
app.run()