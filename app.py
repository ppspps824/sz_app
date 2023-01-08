import streamlit as st
from audio import audio
from paint import paint
from photo import photo
from quiz import quiz
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="KidsApps",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 各種メニューの非表示設定
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


selected = option_menu(
    None,
    ["写真", "録音", "お絵描き", "クイズ"],
    icons=["camera", "mic", "palette", "question-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "写真":
    photo()

if selected == "録音":
    audio()

if selected == "お絵描き":
    paint()

if selected == "クイズ":
    quiz()
