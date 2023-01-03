import streamlit as st
from audio_recorder_streamlit import audio_recorder


def audio():

    # 各種メニューの非表示設定
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden; }
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    #  初期化
    if "audio_list" not in st.session_state:
        st.session_state.audio_list = []

    audio_bytes = False
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.session_state.audio_list.append(audio_bytes)

    with st.sidebar:
        st.write("# 🎙️録った音")
        if st.session_state.audio_list:

            for audio_bytes in st.session_state.audio_list:
                st.audio(audio_bytes, format="audio/wav")
