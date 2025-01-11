import streamlit as st
from connector import service
from utils import image as img_utils
from utils import session as session_utils
from utils import latex as latex_utils

st.title('ExamEasy!')

session_utils.init_session()

n_questions = st.slider("Number of questions", 1, 20, 10)
mood = st.selectbox("Mood", ["Strict", "Neutral", "Friendly and playful"], index=1)
uploaded_files = st.file_uploader("Content to review", type=['png','jpg', 'jpeg', 'gif','webp'], accept_multiple_files=True)
curr_ocr_engine = st.session_state.get("ocr_engine")
curr_llm_model = st.session_state.get("llm_model")
st.write(f"**OCR engine:** {curr_ocr_engine}  |  **LLM:** {curr_llm_model}")

if st.button("Generate"):
    latex = ""
    if curr_ocr_engine == "EasyOCR":
        text = img_utils.uploaded_img_to_text(uploaded_files, 'fr')
        print(text)
        latex = service.generate_mock_exam_from_text(curr_llm_model, text, n_questions, mood)
        print(latex)
    else:
        image_bytes = img_utils.uploaded_img_to_img_bytes(uploaded_files)
        #latex = service.generate_mock_exam_from_images(curr_llm_model, image_bytes, n_questions, mood)

    # pdf_file_location = latex_utils.tex_to_pdf(latex, st.session_state.get("pdflatex_location"))
    # # Open PDF file and load it to memory
    # with open(pdf_file_location, "rb") as f:
    #     pdf_bytes = f.read()
    #     # Close the file
    #     f.close()
    #
    # st.download_button(
    #     label="Download PDF",
    #     data=pdf_bytes,
    #     file_name="mock_exam.pdf",
    #     mime="application/pdf")
