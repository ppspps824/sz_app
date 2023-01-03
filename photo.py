import streamlit as st


def photo():

    # 各種メニューの非表示設定
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden; }
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    #  初期化
    if "pictures" not in st.session_state:
        st.session_state.pictures = []

    picture = False
    picture = st.camera_input(" ")
    if picture:
        st.session_state.pictures.append(picture)

    with st.sidebar:
        st.write("# 📸撮った写真")
        if st.session_state.pictures:
            for picture in st.session_state.pictures:
                st.image(picture)
