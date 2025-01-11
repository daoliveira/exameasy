from langchain_core.messages import HumanMessage
import re
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


def get_llm(model: str):
    if "deepseek" in model:
        llm = ChatOpenAI(temperature=0.1, model_name=model, openai_api_base="https://api.deepseek.com/v1",
                         openai_api_key=st.session_state.deepseek_api_key)
    else:
        llm = ChatOpenAI(temperature=0.1, model_name=model, openai_api_key=st.session_state.openai_api_key)
    return llm


def generate_mock_exam_from_images(model, images, n_questions, mood):

    summary_template = """
        Create a mock exam in the language of the attached material, comprised of {n_questions} questions in different formats 
        (open-ended, close-ended, single-choice, multiple-choice, true-false and association) to test the knowledge 
        of a fifth-grade student on the material attached as images.
        
        Do not mention the question format. For multiple-choice questions, mention the number of correct answers.
        
        Mood: {mood}.
        
        Your response should only contain the mock exam formatted using LaTeX language and after a page break, the 
        expected answers to the mock exam. Use letter document size and 0.5 inches margins for all sides 
        of the document. For open-ended questions, estimate the number of lines required for the answer and draw the 
        lines after the question.
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["n_questions", "mood"], template=summary_template
    )

    filled_prompt = summary_prompt_template.format(n_questions=n_questions, mood=mood)

    content = [{"type": "text", "text": filled_prompt}]
    for image in images:
        content.append({
            "type": "image_url",
            "image_url": {"url": image}
        })
    message = HumanMessage(content=content)

    llm = get_llm(model)

    res = llm.invoke([message])

    # Remove lines starting with three backticks
    result = re.sub(r'^```.*$', '', res.content, flags=re.MULTILINE)

    return result


def generate_mock_exam_from_text(model, text, n_questions, mood):

    summary_template = """
        Create a mock exam in the language of the attached material, comprised of {n_questions} questions in different formats 
        (open-ended, close-ended, single-choice, multiple-choice, true-false and association) to test the knowledge 
        of a fifth-grade student on the material below.
        
        The language of the mock exam should be the same as the language of the material.
        
        Do not mention the question format. For multiple-choice questions, mention the number of correct answers.
        
        Mood: {mood}.
        
        Your response should only contain the mock exam formatted using LaTeX language and after a page break, the 
        expected answers to the mock exam. Use letter document size and 0.5 inches margins for all sides 
        of the document. For open-ended questions, estimate the number of lines required for the answer and draw the 
        lines after the question.
        
        MATERIAL:
        {text}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["n_questions", "mood", "text"], template=summary_template
    )

    filled_prompt = summary_prompt_template.format(n_questions=n_questions, mood=mood, text=text)

    content = [{"type": "text", "text": filled_prompt}]
    message = HumanMessage(content=content)

    llm = get_llm(model)

    res = llm.invoke([message])

    # Remove lines starting with three backticks
    result = re.sub(r'^```.*$', '', res.content, flags=re.MULTILINE)

    return result