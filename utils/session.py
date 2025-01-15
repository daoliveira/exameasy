import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

def init_session():
    if "ocr_engine" not in st.session_state:
        st.session_state.ocr_engine = "EasyOCR"

    if "llm_model" not in st.session_state:
        st.session_state.llm_model = "deepseek-chat"

    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY")

    if "deepseek_api_key" not in st.session_state:
        st.session_state.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
