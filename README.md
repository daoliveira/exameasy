# ExamEasy: AI-Powered Mock Exam Generator

ExamEasy is a Streamlit-based application designed to simplify the process of creating mock exams. By leveraging AI, it 
generates practice exams from study materials uploaded as images. Whether you're a student, teacher, or parent, ExamEasy 
streamlines the creation of custom exams to aid in effective studying.

## How It Works

1. **Text Extraction**: The app uses either **EasyOCR** (a local OCR library) or an **OpenAI vision-enabled model** to 
extract text from uploaded images.
2. **Question Generation**: A generative AI model (DeepSeek, OpenAI, or Llama) processes the extracted text to create a 
mock exam, complete with questions and expected answers.
3. **PDF Generation**: The output is formatted in TeX, and the app uses `pdflatex` to compile it into a downloadable 
PDF file.

## Why ExamEasy?

As a parent, I found myself spending countless hours creating mock exams to help my son prepare for his tests. While I 
initially considered subscribing to OpenAI's vision models for text extraction, I realized a more cost-effective 
solution: combining a local OCR library with a competitively priced generative AI model. ExamEasy was born out of this 
need for an efficient, affordable, and user-friendly tool to automate exam creation.

## Requirements

- a working LaTeX distribution (e.g., TeX Live, MiKTeX) installed and the pdflatex executable in your system's PATH
- deepseek or OpenAI API key

## Installation

```bash
pip install -r requirements.txt
```

Create your .env file with the content below

```text
OPENAI_API_KEY=<if you're using OpenAI models>
DEEPSEEK_API_KEY=<if you're using DeepSeek models>
```

## Usage

```bash
streamlit run app.py
```

## License

MIT

## Author

@daoliveira

