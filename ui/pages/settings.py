import streamlit as st
st.title('Settings')

# OCR Engine Selection
ocr_engine_options = ["EasyOCR", "OpenAI Vision"]
curr_ocr_engine = st.session_state.get("ocr_engine", "EasyOCR")
curr_ocr_engine_idx = ocr_engine_options.index(curr_ocr_engine) if curr_ocr_engine in ocr_engine_options else 0
st.session_state["ocr_engine"] = st.selectbox("OCR Engine", ["EasyOCR", "OpenAI Vision"], curr_ocr_engine_idx)

# LLM Model Selection
llm_model_options = ["deepseek-chat", "gpt-5-mini", "gpt-5-nano"]
if st.session_state["ocr_engine"] == "OpenAI Vision":
    llm_model_options.pop(0) # remove deepseek-chat
curr_llm_model = st.session_state.get("llm_model", "deepseek-chat")
curr_llm_model_idx = llm_model_options.index(curr_llm_model) if curr_llm_model in llm_model_options else 0
st.session_state["llm_model"] = st.selectbox("LLM Model", llm_model_options, curr_llm_model_idx)

# Temperature
# For gpt-5-mini and gpt-5-nano models, set temperature to 1.0 and disable the slider
current_model = st.session_state.get("llm_model", "deepseek-chat")
if current_model in ["gpt-5-mini", "gpt-5-nano"]:
    st.session_state["temperature"] = 1.0
    st.slider("Temperature", 0.0, 1.0, 1.0, 0.1, disabled=True, 
              help="Temperature is fixed at 1.0 for gpt-5-mini and gpt-5-nano models")
else:
    temperature = st.session_state.get("temperature", 0.1)
    st.session_state["temperature"] = st.slider("Temperature", 0.0, 1.0, temperature, 0.1)

# OpenAI API Key
openai_api_key = st.session_state.get("openai_api_key", "")
st.session_state["openai_api_key"] = st.text_input("OpenAI API Key", openai_api_key, type="password")

# DeepSeek API Key
deepseek_api_key = st.session_state.get("deepseek_api_key", "")
st.session_state["deepseek_api_key"] = st.text_input("DeepSeek API Key", deepseek_api_key, type="password")
