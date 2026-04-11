import streamlit as st
import requests
import uuid
import re
import os
import base64
from pathlib import Path

st.set_page_config(page_title="Rossi_Star AI", page_icon="🏂", layout="centered")
st.title("Rossi Star AI")

#Initialization
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcom! I am Rossi Star AI, what can I do for you?\n\n欢迎！我是Rossi Star的AI小助手，我有什么可以帮你的？"}
    ]

#Change the photo
PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = PROJECT_ROOT/"frontend"/"assets"
def render_images(text:str) -> str:
    def replacer(match):
        img_name = match.group(1)
        img_path = os.path.join(IMAGE_DIR, f"{img_name}.png")

        if os.path.exists(img_path):
            with open(img_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()

            html_img = f'<img src="data:image/png;base64,{encoded_string}" style="height: 36px; vertical-align: middle; margin: 0 4px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">'
            return html_img
    
        else:
            return f'Not exist'
    
    return re.sub(r"\[IMAGE:(.*?)\]", replacer, text)

# History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(render_images(msg["content"]), unsafe_allow_html=True)

#Catch input
if user_input := st.chat_input("Please input your question："):
    #Save message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    #Receive reply
    with st.chat_message("assistant"):
        with st.spinner("Rossi Star AI Bot now working..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/chat",
                    json={"query": user_input, "thread_id": st.session_state.thread_id},
                    timeout=30
                )

                if response.status_code == 200:
                    final_answer = response.json()["answer"]

                    st.markdown(render_images(final_answer), unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
        
            except Exception as e:
                st.error(f"error{e}")


