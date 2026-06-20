import base64
import os
import re
import uuid
from pathlib import Path

import requests
import streamlit as st


st.set_page_config(
    page_title="Rossi Star AI",
    page_icon="🏔️",
    layout="centered",
)

st.title("Rossi Star AI")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

FRONTEND_DIR = Path(__file__).resolve().parent
IMAGE_DIR = FRONTEND_DIR / "assets"


def render_images(text: str) -> str:
    def replacer(match):
        img_name = match.group(1).strip()
        img_path = IMAGE_DIR / f"{img_name}.png"

        if img_path.exists():
            with open(img_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

            return (
                f'<img src="data:image/png;base64,{encoded_string}" '
                f'style="max-width:100%; border-radius:10px; margin:8px 0;">'
            )

        return f"`[IMAGE:{img_name}] not found`"

    return re.sub(r"\[IMAGE:(.*?)\]", replacer, text)


if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Welcome! I am Rossi Star AI. What can I do for you?\n\n"
                "欢迎！我是 Rossi Star 的 AI 小助手，我有什么可以帮你的？"
            ),
        }
    ]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(render_images(msg["content"]), unsafe_allow_html=True)


if user_input := st.chat_input("Please input your question:"):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Rossi Star AI Bot is working..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/chat",
                    json={
                        "query": user_input,
                        "thread_id": st.session_state.thread_id,
                    },
                    timeout=180,
                )
                response.raise_for_status()
                final_answer = response.json()["answer"]

                st.markdown(render_images(final_answer), unsafe_allow_html=True)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": final_answer,
                    }
                )

            except Exception as e:
                error_message = f"请求失败：{e}"
                st.error(error_message)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )