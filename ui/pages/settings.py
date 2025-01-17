import streamlit as st
st.title('Settings')

# OCR Engine Selection
ocr_engine_options = ["EasyOCR", "OpenAI Vision"]
curr_ocr_engine = st.session_state.get("ocr_engine", "EasyOCR")
curr_ocr_engine_idx = ocr_engine_options.index(curr_ocr_engine) if curr_ocr_engine in ocr_engine_options else 0
st.session_state["ocr_engine"] = st.selectbox("OCR Engine", ["EasyOCR", "OpenAI Vision"], curr_ocr_engine_idx)

# LLM Model Selection
llm_model_options = ["deepseek-chat", "gpt-4o", "gpt-4o-mini"]
if st.session_state["ocr_engine"] == "OpenAI Vision":
    llm_model_options.pop(0) # remove deepseek-chat
curr_llm_model = st.session_state.get("llm_model", "deepseek-chat")
curr_llm_model_idx = llm_model_options.index(curr_llm_model) if curr_llm_model in llm_model_options else 0
st.session_state["llm_model"] = st.selectbox("LLM Model", llm_model_options, curr_llm_model_idx)

# Temperature
temperature = st.session_state.get("temperature", 0.1)
st.session_state["temperature"] = st.slider("Temperature", 0.0, 1.0, temperature, 0.1)

# OpenAI API Key
openai_api_key = st.session_state.get("openai_api_key", "")
st.session_state["openai_api_key"] = st.text_input("OpenAI API Key", openai_api_key, type="password")

# DeepSeek API Key
deepseek_api_key = st.session_state.get("deepseek_api_key", "")
st.session_state["deepseek_api_key"] = st.text_input("DeepSeek API Key", deepseek_api_key, type="password")
