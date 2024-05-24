import streamlit as st
from tools import picture_sidebar

st.set_page_config(
    page_title="Axes d'améliorations",
    page_icon="🆙",
)

picture_sidebar()

st.markdown("<h1 style='text-align: center;'>Difficultés rencontrées et axes d'améliorations🆙</h1>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>G</span>raphiques 📊</h2>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
- Mettre en avant le **nettoyage des données** avec un avant/après.
- Faire des graphiques plus **dynamiques** et donc plus diversifiés.
""")

st.markdown("---")
st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>M</span>achine Learning 🤖</h2>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
- Difficultés pour le **nettoyage des données**, beaucoup de temps alloué.
- Difficultés de travail dues à des **tables lourdes**.
- Utilisation de Multilabelbinarizer et Hasher pour l'**encoding** et de KNN pour le **machine learning**.
- Avoir une meilleure **organisation** pour les **fichiers partagés** (GitHub).
- Faire un système de recommandation **dédié aux enfants** ou pour **la famille**.
- Améliorer le système de recommandation en ajoutant une **dimension de nationalité** 
  (Ex : comédie française).
""")

st.markdown("---")
st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>S</span>treamlit 👁</h2>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
- Difficultés de **compréhension** et d'**application** de l'outil (language, documentation, API).
- Mettre les recommandations sous **forme d'images**, en ligne (affiche du film).
- Réaliser une **homepage** avec des tops (genres, acteurs.rices, réalisateurs.rices...) pour donner des idées aux utilisateurs.rices.
- **Amélioration de l'interactivité** entre les films recommandés (le film recommandé cliqué devient le film principal et recommande à son tour des films).
""")

st.markdown("---")
st.markdown("<h1 style='text-align: center;'><span style='color:#d38158'>R</span>emerciements🙏🏻</h1>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("<h2 style='text-align: center;'>Merci pour votre écoute 🍿</h2>", unsafe_allow_html=True)

# Chemin vers votre image
chemin_image = "https://image.noelshack.com/fichiers/2024/21/5/1716537074-logo-cine-creuse.png"

# Afficher le logo dans la barre latérale
st.image(chemin_image, width=600)

st.markdown("""
Merci à Teddy et Romain pour leur patience ❤️
""")