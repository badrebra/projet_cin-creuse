import streamlit as st
import pandas as pd
import requests
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction import FeatureHasher
from fuzzywuzzy import process
from tools import picture_sidebar

st.set_page_config(
    page_title="Recommandation",
    page_icon="🎥",
)

picture_sidebar()

# Fonction pour charger les données
def charger_donnees():
    df = pd.read_parquet('Projet_cine_creuse/cine_creuse_table.parquet')
    return df.sort_values(by='popularity', ascending=False)


# Fonction pour récupérer le poster d'un film à partir de l'API TMDb
def recuperer_poster(titre_film):
    api_key = '37e4176ae34cf7d909ee0c57d867d031'
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': titre_film, 'language':'fr'}
    response = requests.get(url, params=params)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        poster_path = data['results'][0]['poster_path']
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return None

# Fonction pour récupérer le tconst d'un film à partir de l'API TMDb
def recuperer_tconst(titre_film):
    df_film=df_ml[df_ml['title']==titre_film]
    return df_film['tconst'].iloc[0]


# Fonction pour récupérer la bande-annonce d'un film à partir de l'API TMDb
def recuperer_bande_annonce(titre_film):
    api_key = '37e4176ae34cf7d909ee0c57d867d031'
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': titre_film, 'language':'fr'}
    response = requests.get(url, params=params)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        movie_id = data['results'][0]['id']
        url_trailer = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}&language=en-US"
        response_trailer = requests.get(url_trailer)
        data_trailer = response_trailer.json()
        if 'results' in data_trailer and len(data_trailer['results']) > 0:
            return data_trailer['results'][0]['key']
    return None

# Fonction pour récupérer la description d'un film à partir de l'API TMDb
def recuperer_description(titre_film):
    api_key = '37e4176ae34cf7d909ee0c57d867d031'
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': titre_film, 'language': 'fr'}
    response = requests.get(url, params=params)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        movie_id = data['results'][0]['id']
        url_movie = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=fr"
        response_movie = requests.get(url_movie)
        data_movie = response_movie.json()
        if 'overview' in data_movie:
            return data_movie['overview']
    return None

# Chargement des données
df = charger_donnees()

st.markdown("<h1 style='text-align: center;'>CINÉ'CREUSE</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sélection des colonnes pour le modèle
df_ml = df[["title", "tconst", "runtimeMinutes", "popularity", "averageRating", "bins_release_date", "genres_y","actor_principal", "name_directors_principal_str","anim", "year"]]

# Mettre le genre en multilabelbinarizer
mlb = MultiLabelBinarizer()
df_genre = pd.DataFrame(mlb.fit_transform(df_ml["genres_y"]), columns=mlb.classes_)
df_ml.reset_index(inplace=True, drop=True)
df_ml = pd.concat([df_ml, df_genre], axis=1)

# Créer un hashing encoder pour la variable actor_principal
hasher_actor = FeatureHasher(n_features=10, input_type='string')
hashed_actor_features = hasher_actor.transform([[actor] for actor in df_ml['actor_principal']])
df_hashed_actor = pd.DataFrame(hashed_actor_features.toarray(), columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])
df_ml = pd.concat([df_ml, df_hashed_actor], axis=1)

# Créer un hashing encoder pour la variable name_directors_principal_str
hasher_director = FeatureHasher(n_features=10, input_type='string')
hashed_director_features = hasher_director.transform([[director] for director in df_ml['name_directors_principal_str']])
df_hashed_director = pd.DataFrame(hashed_director_features.toarray(), columns=["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"])
df_ml = pd.concat([df_ml, df_hashed_director], axis=1)

# Prendre les colonnes numériques pour le modèle
X = df_ml[["averageRating", "bins_release_date","anim",
"a", "b", "c", "d", "e", "f", "g", "h", "i","j", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
"Action","Adventure","Animation","Biography","Comedy","Crime","Drama","Family","Fantasy","History","Horror","Music","Musical",
"Mystery","Romance","Sci-Fi","Sport","Thriller","War","Western"]]


# Choisir et entraîner le modèle
model = NearestNeighbors(n_neighbors=6).fit(X)

# Fonction pour trouver les films les plus proches en utilisant le titre
def find_similar_movies(title):
    # Supprimer les accents et mettre en minuscules
    title = title.lower()

    # Trouver l'index du film correspondant
    index = df_ml[df_ml['title'].str.lower() == title].index
    if index.empty:
        return "Titre non trouvé."

    distances, indices = model.kneighbors(X.iloc[index])

    # Prendre l'indice 1 pour enlever le 0 car le zéro correspond au film de la recherche
    closest_movies_titles = df_ml.loc[indices[0][1:], 'title']

    return closest_movies_titles

# Création de slices sur la variable popularity
bins = [0, 7, 11, 17, 100, 5000]

# Création de labels pour les tranches de popularité
labels = ['⭐', '⭐'*2, '⭐'*3, '⭐'*4, '⭐'*5]

# # Création de la variable tranche_age
df_ml['popularity_star'] = pd.cut(df_ml['popularity'], bins=bins, labels=labels, right=False)

#Sidebar pour entrer le nom du film
st.sidebar.title("Veuillez choisir :")

film_entree = st.sidebar.text_input("Film")

acteur_entree = st.sidebar.text_input("Acteur.rice" )

realisateur_entree = st.sidebar.text_input("Réalisateur.rice" )

#Ajouter un champ pour sélectionner le genre
genre5 = list(df_ml["genres_y"].explode().unique())
genre5.insert(0, ' ')
genre_entree = st.sidebar.selectbox("Genre", options=genre5)

# Si un nom de film est entré
if film_entree != "":
    user_input_normalized = film_entree

    # Utiliser fuzzywuzzy pour trouver le titre le plus proche
    best_match, score, index = process.extractOne(user_input_normalized, df_ml['title'])

    # Récupérer l'index du meilleur match
    matched_index = df_ml[df_ml['title'] == best_match].index[0]

    # Récupérer les données du film sélectionné
    selected_movie_data = df_ml.loc[matched_index]

    # Afficher le film recherché en premier
    titre_film_recherche = selected_movie_data['title']
    poster_url = recuperer_poster(titre_film_recherche)
    bande_annonce_key = recuperer_bande_annonce(titre_film_recherche)
    description = recuperer_description(titre_film_recherche)

    col1, col2 = st.columns([2, 1])  # Ajustez les proportions des colonnes selon vos besoins

    with col1:
        # Center-align the film title
        st.markdown(f"<h2 style='text-align: center;'>{titre_film_recherche}</h2>", unsafe_allow_html=True)

        # Afficher les informations du film
        st.write("**Genre:**", ", ".join(selected_movie_data['genres_y']))
        st.write("**Acteur principal:**", selected_movie_data['actor_principal'])
        st.write(f"**Durée:** {selected_movie_data['runtimeMinutes']} minutes</span>",unsafe_allow_html=True)
        st.write(f"**Date de sortie :** {selected_movie_data['year']}</span>", unsafe_allow_html=True)
        st.write(f"Popularity : ", selected_movie_data['popularity_star'])


        # Affichage de la note moyenne sous forme de rond avec étiquette
        rating_circle = f'<div style="display: flex; flex-direction: row; align-items: center;"><div style="width: 50px; height: 50px; background-color: #28a745; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-size: 12px;">{selected_movie_data["averageRating"]:.1f}</div><div style="margin-left: 10px; color: white; font-size: 14px; font-weight: bold;">Note</div></div>'
        st.markdown(rating_circle, unsafe_allow_html=True)

        if description:
            st.write(description)

        if bande_annonce_key:
            st.write(f"[Voir la bande-annonce](https://www.youtube.com/watch?v={bande_annonce_key})")


    with col2:
        if poster_url:
            st.image(poster_url, width=300)  # Ajustez la largeur de l'image selon vos besoins

    # Trouver les voisins pour le titre correspondant
    distances, indices = model.kneighbors([X.iloc[matched_index].values])

    # Récupérer les titres des films voisins (enlever le film de la recherche lui-même)
    titres_films_proches = df_ml.loc[indices[0][1:], 'title']
    # Ajouter une séparation entre les films
    st.write("---")


    # Afficher les films voisins
    st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>F</span>ilms recommandés : 🎞️</h2>", unsafe_allow_html=True)
    # Ajouter une séparation entre les films
    st.write("---")

    for titre in titres_films_proches:
        # Récupérer les données du film voisin
        matched_index = df_ml[df_ml['title'] == titre].index[0]
        selected_movie_data = df_ml.loc[matched_index]

        # Récupérer les informations du film voisin
        poster_url = recuperer_poster(titre)
        bande_annonce_key = recuperer_bande_annonce(titre)
        description = recuperer_description(titre)

        col1, col2 = st.columns([2, 1])  # Ajustez les proportions des colonnes selon vos besoins

        with col1:
            # Centrer le titre du film voisin
            st.markdown(f"<h2 style='text-align: center;'>{titre}</h2>", unsafe_allow_html=True)

            # Afficher les informations du film
            st.write("**Genre:**", ", ".join(selected_movie_data['genres_y']))
            st.write("**Acteur principal:**", selected_movie_data['actor_principal'])
            st.write(f"**Durée:** {selected_movie_data['runtimeMinutes']} minutes</span>",unsafe_allow_html=True)
            st.write(f"**Date de sortie :** {selected_movie_data['year']}</span>", unsafe_allow_html=True)
            st.write(f"Popularity : ", selected_movie_data['popularity_star'])


            # Affichage de la note moyenne sous forme de rond avec étiquette
            rating_circle = f'<div style="display: flex; flex-direction: row; align-items: center;"><div style="width: 50px; height: 50px; background-color: #28a745; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-size: 12px;">{selected_movie_data["averageRating"]:.1f}</div><div style="margin-left: 10px; color: white; font-size: 14px; font-weight: bold;">Note</div></div>'
            st.markdown(rating_circle, unsafe_allow_html=True)

            if description:
                st.write(description)

            if bande_annonce_key:
                st.write(f"[Voir la bande-annonce](https://www.youtube.com/watch?v={bande_annonce_key})")

        with col2:
            if poster_url:
                # Rendre l'image cliquable
                tconst= recuperer_tconst(titre)
                st.markdown(f'<a href="https://www.imdb.com/title/{tconst}"><img src="{poster_url}" width="300"></a>', unsafe_allow_html=True)

        # Ajouter une séparation entre les films
        st.write("---")

# Si un nom d'acteur est entré
elif acteur_entree != "":
    user_input_normalized = acteur_entree

    # Utiliser fuzzywuzzy pour trouver l'acteur le plus proche
    best_match, score, index = process.extractOne(user_input_normalized, df_ml['actor_principal'])

    # Récupérer l'index du meilleur match
    matched_index = df_ml[df_ml['actor_principal'] == best_match].index[0]

    # Récupérer les films avec cet acteur
    selected_movies_data = df_ml[df_ml['actor_principal'] == best_match]

    # Afficher le nom de l'acteur recherché en premier
    nom_acteur_recherche = selected_movies_data['actor_principal'].iloc[0]
    st.markdown(f"<h2 style='text-align: center;'>Films avec {nom_acteur_recherche}</h2>", unsafe_allow_html=True)

    # Parcourir les films avec l'acteur sélectionné
    for index, movie_data in selected_movies_data.iterrows():
        titre_film = movie_data['title']
        poster_url = recuperer_poster(titre_film)
        bande_annonce_key = recuperer_bande_annonce(titre_film)
        description = recuperer_description(titre_film)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"<h2 style='text-align: center;'>{titre_film}</h2>", unsafe_allow_html=True)
            st.write("**Genre:**", ", ".join(movie_data['genres_y']))


            st.write("**Réalisateur:**", movie_data['name_directors_principal_str'])
            st.write(f"**Durée:** {movie_data['runtimeMinutes']} minutes</span>", unsafe_allow_html=True)
            st.write(f"**Date de sortie :** {movie_data['year']}</span>", unsafe_allow_html=True)
            st.write(f"Popularity : ", movie_data['popularity_star'])

            rating_circle = f'<div style="display: flex; flex-direction: row; align-items: center;"><div style="width: 50px; height: 50px; background-color: #28a745; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-size: 12px;">{movie_data["averageRating"]:.1f}</div><div style="margin-left: 10px; color: white; font-size: 14px; font-weight: bold;">Note</div></div>'
            st.markdown(rating_circle, unsafe_allow_html=True)

            if description:
                st.write(description)

            if bande_annonce_key:
                st.write(f"[Voir la bande-annonce](https://www.youtube.com/watch?v={bande_annonce_key})")

        with col2:
            if poster_url:
                st.image(poster_url, width=300)

        st.write("---")



# Si un nom de réalisateur est entré
elif realisateur_entree != "":
    user_input_normalized = realisateur_entree

    # Utiliser fuzzywuzzy pour trouver le réalisateur le plus proche
    best_match, score, index = process.extractOne(user_input_normalized, df_ml['name_directors_principal_str'])

    # Récupérer l'index du meilleur match
    matched_index = df_ml[df_ml['name_directors_principal_str'] == best_match].index[0]

    # Récupérer les films avec ce réalisateur
    selected_movies_data = df_ml[df_ml['name_directors_principal_str'] == best_match]

    # Afficher le nom du réalisateur recherché en premier
    nom_realisateur_recherche = selected_movies_data['name_directors_principal_str'].iloc[0]
    st.markdown(f"<h2 style='text-align: center;'>Films réalisés par {nom_realisateur_recherche}</h2>", unsafe_allow_html=True)

    # Parcourir les films réalisés par le réalisateur sélectionné
    for index, movie_data in selected_movies_data.iterrows():
        titre_film = movie_data['title']
        poster_url = recuperer_poster(titre_film)
        bande_annonce_key = recuperer_bande_annonce(titre_film)
        description = recuperer_description(titre_film)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"<h2 style='text-align: center;'>{titre_film}</h2>", unsafe_allow_html=True)
            st.write("**Genre:**", ", ".join(movie_data['genres_y']))

            st.write("**Réalisateur:**", movie_data['name_directors_principal_str'])
            st.write(f"**Durée:** {movie_data['runtimeMinutes']} minutes</span>", unsafe_allow_html=True)
            st.write(f"**Date de sortie :** {movie_data['year']}</span>", unsafe_allow_html=True)
            st.write(f"Popularity : ", movie_data['popularity_star'])

            rating_circle = f'<div style="display: flex; flex-direction: row; align-items: center;"><div style="width: 50px; height: 50px; background-color: #28a745; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-size: 12px;">{movie_data["averageRating"]:.1f}</div><div style="margin-left: 10px; color: white; font-size: 14px; font-weight: bold;">Note</div></div>'
            st.markdown(rating_circle, unsafe_allow_html=True)

            if description:
                st.write(description)

            if bande_annonce_key:
                st.write(f"[Voir la bande-annonce](https://www.youtube.com/watch?v={bande_annonce_key})")

        with col2:
            if poster_url:
                st.image(poster_url, width=300)

        st.write("---")



elif genre_entree != " ":

    # Filtrer les films par genre
    selected_movies_data = df_ml[df_ml['genres_y'].map(lambda x: genre_entree in x)]
    print("------------------------------------------------")
    print(selected_movies_data)
    print("genre entré: ", genre_entree)

    # Afficher les films du genre sélectionné
    if not selected_movies_data.empty:
        st.markdown(f"<h2 style='text-align: center;'>Films du genre {genre_entree}</h2>", unsafe_allow_html=True)

        # Parcourir les films du genre sélectionné
        for index, movie_data in selected_movies_data.head(10).iterrows():
            titre_film = movie_data['title']
            poster_url = recuperer_poster(titre_film)
            bande_annonce_key = recuperer_bande_annonce(titre_film)
            description = recuperer_description(titre_film)

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"<h2 style='text-align: center;'>{titre_film}</h2>", unsafe_allow_html=True)
                st.write("**Genre:**", ", ".join(movie_data['genres_y']))

                st.write("**Réalisateur:**", movie_data.get('name_directors_principal_str', 'Inconnu'))
                st.write(f"**Durée:** {movie_data.get('runtimeMinutes', 'Inconnu')} minutes</span>", unsafe_allow_html=True)
                st.write(f"**Date de sortie :** {movie_data['year']}</span>", unsafe_allow_html=True)
                st.write(f"Popularity : ", movie_data['popularity_star'])


                if 'averageRating' in movie_data:
                    rating_circle = f'<div style="display: flex; flex-direction: row; align-items: center;"><div style="width: 50px; height: 50px; background-color: #28a745; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-size: 12px;">{movie_data["averageRating"]:.1f}</div><div style="margin-left: 10px; color: white; font-size: 14px; font-weight: bold;">Note</div></div>'
                    st.markdown(rating_circle, unsafe_allow_html=True)

                if description:
                    st.write(description)

                if bande_annonce_key:
                    st.write(f"[Voir la bande-annonce](https://www.youtube.com/watch?v={bande_annonce_key})")

            with col2:
                if poster_url:
                    st.image(poster_url, width=300)

            st.write("---")
