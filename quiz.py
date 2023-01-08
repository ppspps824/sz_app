import base64
import glob
import random
import time

import streamlit as st
from st_clickable_images import clickable_images


def quiz():
    container = st.empty()

    def judge(clicked, correct, page_id):
        if clicked == correct:
            time.sleep(0.5)
            st.markdown(st.session_state.correct_sound_html, unsafe_allow_html=True)
            st.balloons()
            st.session_state.correct_num += 1
        else:
            time.sleep(0.5)
            st.markdown(st.session_state.failed_sound_html, unsafe_allow_html=True)

        st.session_state.page_id = page_id
        st.session_state.first = True

    def quest(no):
        st.markdown(
            f"<h1 style='text-align: center;'>第{no}問</h1>",
            unsafe_allow_html=True,
        )

        if st.session_state.first:
            st.session_state.questions = [0] * 2
            st.session_state.correct, st.session_state.failed = random.sample([0, 1], 2)
            st.session_state.questions[st.session_state.correct] = random.choice(
                st.session_state.cat_images
            )
            st.session_state.questions[st.session_state.failed] = random.choice(
                st.session_state.dog_images
            )
            st.session_state.first = False

        clicked = clickable_images(
            st.session_state.questions,
            titles=[f"Image#{str(i)}" for i in range(2)],
            div_style={
                "display": "flex",
                "justify-content": "center",
                "flex-wrap": "wrap",
            },
            img_style={"margin": "5px", "height": "400px"},
            key=no,
        )

        if clicked > -1:
            if no != st.session_state.quest_num:
                judge(clicked, st.session_state.correct, f"page{no+1}")
            else:
                judge(clicked, st.session_state.correct, "final")
        else:
            st.stop()

    if "page_id" not in st.session_state:
        cat_files = glob.glob("./assets/image/cat/*")
        dog_files = glob.glob("./assets/image/dog/*")
        start_image = "./assets/image/start.png"
        again_image = "./assets/image/again.jpg"

        st.session_state.sounds = {
            "correct": "./assets/audio/correct.mp3",
            "failed": "./assets/audio/failed.mp3",
        }
        with open(st.session_state.sounds["correct"], "rb") as file1:
            audio_str = "data:audio/ogg;base64,%s" % (
                base64.b64encode(file1.read()).decode()
            )
            st.session_state.correct_sound_html = (
                """
                        <audio autoplay=True>
                        <source src="%s" type="audio/ogg" autoplay=True>
                        Your browser does not support the audio element.
                        </audio>
                    """
                % audio_str
            )

        with open(st.session_state.sounds["failed"], "rb") as file2:
            audio_str = "data:audio/ogg;base64,%s" % (
                base64.b64encode(file2.read()).decode()
            )
            st.session_state.failed_sound_html = (
                """
                        <audio autoplay=True>
                        <source src="%s" type="audio/ogg" autoplay=True>
                        Your browser does not support the audio element.
                        </audio>
                    """
                % audio_str
            )

        st.session_state.cat_images = []
        for file1 in cat_files:
            with open(file1, "rb") as image1:
                encoded = base64.b64encode(image1.read()).decode()
                st.session_state.cat_images.append(f"data:image/jpeg;base64,{encoded}")

        st.session_state.dog_images = []
        for file2 in dog_files:
            with open(file2, "rb") as image2:
                encoded = base64.b64encode(image2.read()).decode()
                st.session_state.dog_images.append(f"data:image/jpeg;base64,{encoded}")

        with open(start_image, "rb") as image3:
            encoded = base64.b64encode(image3.read()).decode()
            st.session_state.start_logo = f"data:image/jpeg;base64,{encoded}"

        with open(again_image, "rb") as image4:
            encoded = base64.b64encode(image4.read()).decode()
            st.session_state.again_logo = f"data:image/jpeg;base64,{encoded}"

        st.session_state.correct_num = 0
        st.session_state.first = True
        st.session_state.page_id = "main"

    if st.session_state.page_id == "main":
        with container.container():
            st.markdown(
                "<h1 style='text-align: center;'>どっちがしずくでしょう？？</h1>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h3 style='text-align: center;'>問題数</h3>",
                unsafe_allow_html=True,
            )
            _, _, center, _, _ = st.columns(5)
            with center:
                st.session_state.quest_num = int(
                    st.radio(" ", ("3", "5", "10"), horizontal=True)
                )
            clicked = clickable_images(
                [st.session_state.start_logo],
                titles=[f"Image#{str(i)}" for i in range(1)],
                div_style={
                    "display": "flex",
                    "justify-content": "center",
                    "flex-wrap": "wrap",
                },
                img_style={"margin": "5px", "height": "200px"},
                key="top",
            )

            if clicked == 0:
                st.session_state.page_id = "page1"
                st.experimental_rerun()

    for num in range(st.session_state.quest_num):
        if st.session_state.page_id == f"page{num+1}":
            with container.container():
                quest(num + 1)

    if st.session_state.page_id == "final":
        with container.container():
            st.markdown(
                "<h1 style='text-align: center;'>結果</h1>",
                unsafe_allow_html=True,
            )
            time.sleep(1)
            st.markdown(
                f"<h1 style='text-align: center;'>{st.session_state.correct_num}問正解！！</h1>",
                unsafe_allow_html=True,
            )
            clicked = clickable_images(
                [st.session_state.again_logo],
                titles=[f"Image#{str(i)}" for i in range(1)],
                div_style={
                    "display": "flex",
                    "justify-content": "center",
                    "flex-wrap": "wrap",
                },
                img_style={"margin": "5px", "height": "200px"},
                key="final",
            )

            if clicked == 0:
                st.session_state.pop("page_id")
                st.experimental_rerun()
