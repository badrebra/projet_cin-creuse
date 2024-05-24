import streamlit as st
import pandas as pd
import plotly.express as px
from tools import picture_sidebar

st.set_page_config(
    page_title="Graphiques",
    page_icon="📊",
)

picture_sidebar()

# Assuming your data is loaded into a pandas dataframe named 'df'
df = pd.read_parquet('Projet_cine_creuse/cine_creuse_table.parquet')

# H1 centré
st.markdown("<h1 style='text-align: center;'>Présentation & Analyse du dataset🎬</h1>", unsafe_allow_html=True)

# H2 centré
st.markdown("---")
st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>G</span>énéralités du Dataset 🍿</h2>", unsafe_allow_html=True)
st.markdown("---")

# Pour centré les 2 phrases descriptives
st.markdown("""
<div style='text-align: center;'>
    <p>7586 Films</p>
    <p>Films uniquement diffusés en France</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Création de l'histogramme "Répartition des films par catégorie"
genre = df["genres_y"].explode()
fig_genre = px.histogram(
    x=genre,
    color_discrete_sequence=px.colors.qualitative.Safe,
    labels={'x': "Genres"},
    title='Répartition des films par catégories'
)
fig_genre.update_yaxes(title_text='Nombre de films')
fig_genre.update_layout(title_x=0.2,
                        xaxis=dict(tickangle=45))

# Création de l'histogramme "Durée par genre"
explode_genres = df.explode("genres_y")
genre_duration = explode_genres.groupby("genres_y")["runtimeMinutes"].mean().reset_index()
top_genre_durations = genre_duration.sort_values(by="runtimeMinutes", ascending=False).head(10)
fig_duree_genre = px.bar(
    top_genre_durations, 
    x="genres_y", 
    y="runtimeMinutes",
    color_discrete_sequence=px.colors.qualitative.Safe,
    labels={'genres_y': 'Genres', 'runtimeMinutes': 'Durée moyenne (minutes)'},
    title='Durée moyenne des films par genre'
)
fig_duree_genre.update_layout(title_x=0.2,
                              xaxis=dict(tickangle=45))

# Disposition des graphiques
col1, col2 = st.columns(2)

# Afficher les graphiques côte à côte
with col1:
    st.plotly_chart(fig_genre, use_container_width=True)
    st.markdown("**Critères de tri**""""
- Suppression des genres peu diffusés au cinéma (Documentaires, Feuilletons TV, Films pour adultes).
- Adaptation des genres selon les caractéristiques de la population de la Creuse.
""")

with col2:
    st.plotly_chart(fig_duree_genre, use_container_width=True)
    st.markdown("**Critères de tri**""""
- Durée des films compris entre 80 et 210 minutes.
- Les films d'animations sont souvent moins longs.
- Certains films cultes sont très longs.
""")
    
st.markdown("---")

# Créer un diagramme de dispersion durée des films par années
fig_duree = px.scatter(
    df, 
    x="release_date", 
    y="runtimeMinutes", 
    color_discrete_sequence=px.colors.qualitative.Safe,
    labels={'release_date': 'Années', 'runtimeMinutes': 'Durée moyenne (minutes)'},
    title="Durée des films par année"
)
fig_duree.update_layout(title_x=0.3)
st.plotly_chart(fig_duree)

st.markdown("**Critère de tri**""""
- Plage de dates 1980 - 2024.
""")

st.markdown("---")

# Création d'un graphique "Les films les mieux notés"
df_top_vote = df[df['numVotes'] > 1000000]
df_top_5 = df_top_vote[['title', 'averageRating', 'numVotes', 'name_directors_principal_str', 'actor_principal' ]].sort_values(by='averageRating',  ascending=False).head(5)
# Définir la longueur max des str pour la colonne title
max_title_length = 35
# Couper les titres à la longueur maximale souhaitée
df_top_5['title'] = df_top_5['title'].str.slice(0, max_title_length)

df_top_5['hover_info'] = df_top_5['name_directors_principal_str'] + ' - ' + df_top_5['actor_principal']
fig_top_5 = px.bar(
    df_top_5,
    x="title",
    y="averageRating",
    color_discrete_sequence=px.colors.qualitative.Safe,
    hover_name='hover_info',
    labels={'title': 'Titre du film', 'averageRating': 'Moyenne des notes'},
    title='Les 5 meilleurs films avec les réalisateurs et acteurs'
)
fig_top_5.update_layout(title_x=0.1)
st.plotly_chart(fig_top_5)

st.markdown("**Critère de tri**""""
- Films ayant au minimum 6.5/10 de moyenne.
""")

st.markdown("---")
st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>L</span>es Acteurs.rices 📺</h2>", unsafe_allow_html=True)

# Création de l'histogramme "Acteurs les mieux noté"
actor_counts = df["meilleur_acteur"].explode().value_counts().head(10)
actors_df = actor_counts.reset_index()
actors_df.columns = ['Actors', 'Count']
fig_act_note = px.bar(
    actors_df, 
    x='Actors', 
    y='Count', 
    color_discrete_sequence=px.colors.qualitative.Alphabet, 
    labels={'Actors': 'Acteurs.rices', 'Count': 'Nombre de films'}, 
    title='Top 10 des acteurs.rices<br>les mieux notés'
)
fig_act_note.update_layout(
    xaxis=dict(tickangle=45),
    title={
        'text': 'Top 10 des acteurs.rices<br>les mieux notés',
        'x': 0.6,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

st.markdown("---")

# Création de l'histogramme "Acteurs les plus présent"
actor_counts = df["primaryName"].explode().value_counts().head(10)
actors_df = actor_counts.reset_index()
actors_df.columns = ['Actor', 'Count']
fig_act_present = px.bar(
    actors_df, 
    x='Actor', 
    y='Count', 
    color_discrete_sequence=px.colors.qualitative.Alphabet, 
    labels={'Actor': 'Acteurs.rices', 'Count': 'Nombre de films'}, 
    title='Top 10 des acteurs.rices<br>ayant joué dans le plus de films'
)
fig_act_present.update_layout(
    xaxis=dict(tickangle=45),
    title={
        'text': 'Top 10 des acteurs.rices<br>ayant joué dans le plus de films',
        'x': 0.6,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

col1, col2 = st.columns(2)

# Afficher les graphiques côte à côte

with col1:
    st.plotly_chart(fig_act_note, use_container_width=True)

with col2:
    st.plotly_chart(fig_act_present, use_container_width=True)

# Création de l'histogramme "Réalisateurs les plus présents"
director_counts = df["name_directors"].explode().value_counts().head(10)
directors_df = director_counts.reset_index()
directors_df.columns = ['Directors', 'Count']
fig_real = px.bar(
    directors_df, 
    x='Directors', 
    y='Count', 
    color_discrete_sequence=["pink"], 
    labels={'Directors': 'Réalisateurs.rices', 'Count': 'Nombre de films'}, 
    title='Les réalisateurs.rices<br>ayant produit le plus de films'
)
fig_real.update_layout(
    xaxis=dict(tickangle=45),
    title={
        'text': 'Les réalisateurs.rices<br>ayant produit le plus de films',
        'x': 0.6,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

# Création de l'histogramme "Maisons de production"
production_counts = df["production_companies_name"].explode().value_counts().head(10)
production_df = production_counts.reset_index()
production_df.columns = ['Production Companies', 'Count']
fig_prod = px.bar(
    production_df, 
    x='Production Companies',
    y='Count',
    color_discrete_sequence=["violet"],
    labels={'Production Companies': "Maisons de production" , 'Count': 'Nombre de films'},
    title='Nombre de films par<br>maisons de production'
)
fig_prod.update_layout(
    xaxis=dict(tickangle=45),
    title={
        'text': 'Nombre de films par<br>maisons de production',
        'x': 0.6,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

# Disposition des sous-titres et graphiques côte à côte
col1, col2 = st.columns(2)

with col1:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>L</span>es Réalisateurs<br>.rices 📽️</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.plotly_chart(fig_real, use_container_width=True)

with col2:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>L</span>es maisons de production 🎞️</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.plotly_chart(fig_prod, use_container_width=True)

st.markdown("---")
st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>C</span>onclusion ✅</h2>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
- **Actuellement :**
            Dataset qui comprend des films divers (Genres, Dates, Maisons de production...).
- **À venir :**
            Analyser la recherche des clients pour comprendre leurs préférences afin que le CINÉ'CREUSE puisse les exploiter.
""")
