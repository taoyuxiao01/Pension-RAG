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
IMAGE_DISPLAY_WIDTH = int(os.getenv("IMAGE_DISPLAY_WIDTH", "96"))
IMAGE_TAG_PATTERN = re.compile(
    r"`?\[(?:IMAGE|IMGAE)\s*[:：]\s*([^\]]+?)\]`?",
    flags=re.IGNORECASE,
)


def find_image_path(img_name: str) -> Path | None:
    clean_name = img_name.strip().strip("`")
    img_path = IMAGE_DIR / f"{clean_name}.png"

    if img_path.exists():
        return img_path

    return next(
        (
            asset
            for asset in IMAGE_DIR.glob("*.png")
            if asset.stem.lower() == clean_name.lower()
        ),
        None,
    )


def render_message(text: str) -> None:
    last_end = 0

    for match in IMAGE_TAG_PATTERN.finditer(text):
        before = text[last_end : match.start()]
        if before.strip():
            st.markdown(before)

        img_name = match.group(1)
        img_path = find_image_path(img_name)

        if img_path:
            st.image(str(img_path), width=IMAGE_DISPLAY_WIDTH)
        else:
            st.markdown(f"`[IMAGE:{img_name.strip()}] not found`")

        last_end = match.end()

    remaining = text[last_end:]
    if remaining.strip():
        st.markdown(remaining)


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
        render_message(msg["content"])


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

                render_message(final_answer)

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
