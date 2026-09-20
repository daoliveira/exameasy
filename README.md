# ExamEasy: AI-Powered Mock Exam Generator

ExamEasy is a Streamlit-based application designed to simplify the process of creating mock exams. By leveraging AI, it 
generates practice exams from study materials uploaded as images. Whether you're a student, teacher, or parent, ExamEasy 
streamlines the creation of custom exams to aid in effective studying.

## How It Works

1. **Text Extraction**: The app uses either **EasyOCR** (a local OCR library) or **LLM Vision**, which
sends the images directly to a vision-capable model (DeepSeek `deepseek-flash`, OpenAI `gpt-5-mini`/
`gpt-5-nano`, or Google `gemini-2.5-pro`).
2. **Question Generation**: The selected model (DeepSeek, OpenAI, or Google Gemini) processes the 
material to create a mock exam, complete with questions and expected answers.
3. **PDF Generation**: The output is formatted in TeX, and the app uses `pdflatex` to compile it into a downloadable 
PDF file.

## Why ExamEasy?

As a parent, I found myself spending countless hours creating mock exams to help my son prepare for his tests. While I 
initially considered subscribing to OpenAI's vision models for text extraction, I realized a more cost-effective 
solution: combining a local OCR library with a competitively priced generative AI model. ExamEasy was born out of this 
need for an efficient, affordable, and user-friendly tool to automate exam creation.

## Requirements

- a working LaTeX distribution (e.g. TeX Live, MiKTeX) installed and the pdflatex executable in your system's PATH
- at least one API key: DeepSeek (default), OpenAI, or Google
- Python 3.12+

## Installation

```bash
pip install -r requirements.txt
```

Create your .env file with the content below

```text
OPENAI_API_KEY=<if you're using OpenAI models>
DEEPSEEK_API_KEY=<if you're using DeepSeek models>
GOOGLE_API_KEY=<if you're using Google Gemini models>
```

## Usage

```bash
python -m streamlit run ui/app.py
```

Then open http://localhost:8501.

## Configuration

Settings are available on the **Settings** page:

- **OCR engine**: `EasyOCR` (runs locally; requires selecting the document language) or `LLM Vision`
  (sends images to the selected LLM).
- **LLM model**: `deepseek-flash` (default, DeepSeek-V4.1-Flash), `gpt-5-mini`, `gpt-5-nano`,
  or `gemini-2.5-pro`.
- **Temperature**, plus the API keys for each provider.

On the main page you choose the number of questions (1-20), the exam mood, and the school year
(7th Grade by default).

Supported upload formats: **JPEG, PNG, GIF, and WebP**.

> **Note:** For DeepSeek, `deepseek-flash` is the vision-capable model. Images are automatically
> downscaled and re-encoded before being sent, and a request is blocked with a clear error if the
> batch would exceed DeepSeek's 48 MiB request limit.

## License

MIT

## Author

@daoliveira

