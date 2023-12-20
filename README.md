![Logo.png](https://github.com/JavierEdgarEsteban77/Proy-Ind-N--1-MLOps/blob/fae94f5b470f3ed9d5f607280a40f9c276afd92a/Logo.png)

***Descripción del Proyecto***

Este proyecto consiste en un análisis de datos de juegos de la empresa Steam, con reseñas de usuarios y datos de usuarios, entre otros.

El objetivo es realizar ingeniería de características, análisis de sentimientos y desarrollo de una API para disponibilizar los datos cuya finalidad es obtener el Producto Mínimo Viable (MVP) y brindar todas las recomendaciones necesarias para brindar información para la toma de decisiones.

Previamente analizaremos el estado de los datasets, los limpiaremos, normalizaremos para trabajar con las librerías y herramientas necesarias para poder procesar toda la inforamción que necesita la empresa.

***Requisitos***

- Python 3.12.0
- Pandas
- NLTK
- Matplotlib
- FastAPI.

**Archivos del Proyecto en el cual trabajaremos para armar nuestros DataFrames de Steam.**

- Este archivo contiene los datos de los juegos: steam_games.json
- Este archivo contiene las reseñas de los usuarios: user_reviews.json.gz
- Este archivo contiene los datos de los usuarios: users_items.json.gz

Además, se han creado los siguientes archivos CSV a partir de los DataFrames con los que se ha trabajado y están disponibles en el repositorio clonado:
- steam_games.csv
- user_reviews.csv
- users_items.csv

- Los archivos JSON estarán disponibilizados para solo lectura en el siguiente enlace: https://1drv.ms/f/s!AhToA3u1i9cWgbgRX1-IzjbRp3sxTQ?e=LOY0Yy

**Proceso a ejecutar el código en este orden:**

1. Importamos las bibliotecas necesarias, éstas son: json, pandas, ast, gzip, nltk, vader_lexicon, matplotlib, seaborn, boxplot, os, FastAPI, tqdm.
2. Adaptamos nuestros dataset en los siguientes DataFrames en los que trabajaremos: `df_steam_games`, `df_user_reviews_desanidado`, `df_users_items_desanidado`.
3. Cargamos y trabajamos los datos de los juegos de Steam, las reseñas de los usuarios y los datos de los usuarios utilizando la función `cargar_datos` para poder procesarlos.
4. Realizamos el preprocesamiento y la limpieza de los datos.
5. Realizamos el análisis de sentimientos en las reseñas de los usuarios utilizando la biblioteca NLTK.

**Sistema de Recomendación**

El sistema de recomendación que se utilizará en este proyecto es de tipo user-item. 

Este tipo de sistema toma un usuario, encuentra usuarios similares y recomienda ítems que a esos usuarios similares les gustaron. En este caso, el input es un usuario y el output es una lista de juegos que se le recomienda a ese usuario.

**Desarrollo de una API utilizando FastAPI con los siguientes endpoints:**

- PlayTimeGenre(genero: str): Este endpoint devuelve un diccionario que contiene el año con más horas jugadas para el género especificado.

- UserForGenre(genero: str): Este endpoint devuelve un diccionario que contiene el usuario que ha jugado más horas para el género especificado y una lista de diccionarios que representa la acumulación de horas jugadas por año.

- UsersRecommend(año: int): Este endpoint devuelve una lista de diccionarios que contiene el top 3 de juegos más recomendados por usuarios para el año especificado.

- UsersWorstDeveloper(año: int): Este endpoint devuelve una lista de diccionarios que contiene el top 3 de desarrolladoras con juegos menos recomendados por usuarios para ese año.

- sentiment_analysis(empresa desarrolladora: str): Este endpoint devuelve un diccionario que contiene el nombre de la empresa desarrolladora como llave y una lista de strings con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.

**Ejecución de la API**

Para ejecutar la API, se debe correr el archivo api_steam.py.

**Video Explicativo**

Enlace al video explicativo: (El enlace se agregará cuando el video esté listo)

**Notas**

Es menester considerar que este proyecto puede ser mejorado y ampliado en el futuro cuya finalidad es brindar información oportuna para la toma de decisiones.
