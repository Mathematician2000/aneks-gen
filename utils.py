import streamlit as st


def set_background(url: str) -> None:
    css_style = rf'''
        <style>
          .stApp {{
            background-image: url("{url}");
            background-size: 100%;
          }}
        </style>
    '''
    st.markdown(css_style, unsafe_allow_html=True)
