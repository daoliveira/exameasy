import streamlit as st
from connector import service
from utils import image as img_utils
from utils import session as session_utils
from utils import latex as latex_utils
from utils.easyocr import EASYOCR_LANG_MAP, get_lang_name

st.set_page_config(page_title="ExamEasy!")
st.title('ExamEasy!')

session_utils.init_session()

MOOD_LIST = ["Strict", "Neutral", "Friendly and playful"]

SCHOOL_YEAR_LIST = ["1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade", "6th Grade", "7th Grade",
                    "8th Grade", "9th Grade", "10th Grade", "11th Grade", "12th Grade", "University"]

st.markdown("""
    Welcome to ExamEasy! This app helps you generate mock exams from your notes.
    Upload your notes, select the number of questions and the mood of the exam, and let the magic happen!
""")

n_questions = st.slider("Number of questions", 1, 20, 10)
col = st.columns(2)
mood = col[0].selectbox("Mood", MOOD_LIST, index=1)
school_year = col[1].selectbox("School year", SCHOOL_YEAR_LIST, index=4)

uploaded_files = st.file_uploader("Content to review", type=['jpg', 'jpeg'], accept_multiple_files=True)

curr_ocr_engine = st.session_state.get("ocr_engine")
curr_llm_model = st.session_state.get("llm_model")

# add a selector for language
if curr_ocr_engine == "EasyOCR":
    ocr_lang = st.selectbox(
        "Language",
        options=list(EASYOCR_LANG_MAP.keys()),
        format_func=get_lang_name,
        index=26,
        help="EasyOCR requires knowledge of the language of the text to be recognized.")

st.caption(f"**OCR engine:** {curr_ocr_engine}  |  **LLM:** {curr_llm_model}  |  **Temperature:** {st.session_state.temperature}",
           help="You can change these in settings")

if st.button("Generate"):
    # Add a streamlit status gadget
    st_status = st.status("Generating mock exam...")

    latex = ""
    if curr_ocr_engine == "EasyOCR":
        st_status.update(label="Extracting text from images...")
        text = img_utils.uploaded_img_to_text(st_status, uploaded_files, ocr_lang)
        st_status.update(label="Calling LLM to generate mock exam...")
        latex = service.generate_mock_exam_from_text(text, curr_llm_model, n_questions, mood, school_year)
    else:
        st_status.update(label="Calling LLM to generate mock exam...")
        image_bytes = img_utils.uploaded_img_to_img_bytes(uploaded_files)
        latex = service.generate_mock_exam_from_images(image_bytes, curr_llm_model, n_questions, mood, school_year)

    # Convert TeX string to PDF bytes
    st_status.update(label="Mock exam generated. Converting to PDF...")
    try:
        pdf_bytes = latex_utils.latex_to_pdf(latex)
        st_status.update(label="PDF generated!", state="complete")
    except Exception as e:
        st_status.update(label="Error generating the PDF. Try fixing the LaTeX file manually or click Generate again.", state="error")
        pdf_bytes = None

    @st.fragment
    def download_buttons():
        btn_col = st.columns(2)
        btn_col[0].download_button(
            label="Download TeX",
            data=latex,
            file_name="mock_exam.tex",
            mime="text/plain")
        if pdf_bytes is not None:
            btn_col[1].download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="mock_exam.pdf",
                mime="application/pdf")

    download_buttons()
