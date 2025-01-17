from langchain_core.messages import HumanMessage
import re
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


def get_llm(model: str):
    if "deepseek" in model:
        llm = ChatOpenAI(temperature=st.session_state.temperature, model_name=model, openai_api_base="https://api.deepseek.com/v1",
                         openai_api_key=st.session_state.deepseek_api_key)
    else:
        llm = ChatOpenAI(temperature=st.session_state.temperature, model_name=model, openai_api_key=st.session_state.openai_api_key)
    return llm


def generate_mock_exam(content, model, n_questions, mood, school_year):
    summary_template = """
        Create a mock exam in the language of the attached material, comprised of {n_questions} questions in different formats 
        (open-ended, close-ended, single-choice, multiple-choice, true-false and association) to test the knowledge 
        of a {school_year} student on the material attached.
        
        Do not mention the question format. For multiple-choice questions, mention the number of correct answers.
        
        Mood: {mood}.
        
        Your response should only contain the mock exam formatted using LaTeX language. Make sure to add all required
        packages for the commands included in the LaTeX document. After a page break add the 
        expected answers to the mock exam. Use letter document size and 0.5 inches margins for all sides 
        of the document. For open-ended questions, estimate the number of lines required for the answer and draw the 
        lines after the question.
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["n_questions", "mood", "school_year"], template=summary_template
    )

    filled_prompt = summary_prompt_template.format(n_questions=n_questions, mood=mood, school_year=school_year)

    content = [{"type": "text", "text": filled_prompt}] + content
    message = HumanMessage(content=content)

    llm = get_llm(model)

    res = llm.invoke([message])

    # check if res has attribute content
    if hasattr(res, 'content'):
        res = res.content
    else:
        res = res

    # Remove lines starting with three backticks (sometimes OpenAI generate these)
    result = re.sub(r'^```.*$', '', res, flags=re.MULTILINE)

    return result

def generate_mock_exam_from_images(images, model, n_questions, mood, school_year):
    content = []
    for image in images:
        content.append({
            "type": "image_url",
            "image_url": {"url": image}
        })
    return generate_mock_exam(content, model, n_questions, mood, school_year)

def generate_mock_exam_from_text(text, model, n_questions, mood, school_year):
    content = [{"type": "text", "text": text}]
    return generate_mock_exam(content, model, n_questions, mood, school_year)
