import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas


def paint():
    def save_paint():
        st.session_state.paint_list.append(canvas_result.image_data)

    # 各種メニューの非表示設定
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden; }
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    #  初期化
    if "paint_list" not in st.session_state:
        st.session_state.paint_list = []

    # Specify canvas parameters in application
    drawing_mode = st.sidebar.selectbox("Drawing tool:", ("freedraw", "transform"))

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == "point":
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=400,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == "point" else 0,
        key="canvas",
    )

    st.button("保存", on_click=save_paint)

    with st.sidebar:
        st.write("# 🎨描いた絵")
        for paint in st.session_state.paint_list:
            st.image(paint)
