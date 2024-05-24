import streamlit as st
from tools import picture_sidebar

st.set_page_config(
    page_title="Homepage",
    page_icon="🏚️",
)

picture_sidebar()

st.markdown("<h1 style='text-align: center;'>Projet CINÉ'CREUSE🎬</h1>", unsafe_allow_html=True)

# H2 Concept
st.markdown("---")
st.markdown("""
<h2 style='text-align: center;'><span style='color:#d38158'>C</span>oncept 📋</h2>
""", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
Un **cinéma** en perte de vitesse situé dans la **Creuse** a décidé de passer le cap du **digital** en créant un site Internet taillé pour les locaux...  
Dans un premier temps le client souhaite avoir la **visualisation** du dataset et des **statistiques**.  
Puis il souhaite créer un moteur de recherche de **recommandation de film**.
""")

# H2 L'équipe
st.markdown("---")
st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>L</span>'équipe 👥👥</h2>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
<div style='text-align: center;'>
<strong>V</strong>éronique<br>
<strong>B</strong>rahim<br>
<strong>M</strong>elvin<br>
<strong>M</strong>arion
</div>
""", unsafe_allow_html=True)

# H2 Les outils
st.markdown("---")
st.markdown("<h2 style='text-align: center;'><span style='color:#d38158'>L</span>es outils 🛠️</h2>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
- Dataset : **Imdb / Tmdb**
- Language de programmation : **Python, HTML, CSS**
- Éditeur de texte : **VS Code**
- Application web : **Streamlit**
- **Hébergeur** photo
""")