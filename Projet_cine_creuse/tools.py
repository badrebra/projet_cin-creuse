import streamlit as st

def picture_sidebar():
  st.markdown(
      """
      <style>
          [data-testid="stSidebarNav"] {
              background-image: url(https://image.noelshack.com/fichiers/2024/21/5/1716537074-logo-cine-creuse.png);
              background-repeat: no-repeat;
              padding-top: 140px;
              background-position: 70px 20px;
              background-size:180px 180px
          }
      </style>
      """,
      unsafe_allow_html=True,
  )