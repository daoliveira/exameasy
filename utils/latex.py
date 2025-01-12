import uuid
import subprocess
import tempfile
import os

def latex_to_pdf(tex):
    """
    Converts a LaTeX file to a PDF using pdflatex.

    Args:
        tex: Contents of the LaTeX file as a string.

    Returns:
        PDF bytes on success, None on failure (e.g., pdflatex errors).
        Raises FileNotFoundError if pdflatex does not exist.
        Raises RuntimeError if pdflatex is not installed or if there is a problem during compilation.
    """
    file_name = str(uuid.uuid4())
    tex_file = f'{file_name}.tex'
    pdf_file = f'{file_name}.pdf'

    try:
        # Use a temporary directory to avoid cluttering the current directory
        with tempfile.TemporaryDirectory("tmp") as temp_dir:
            # Write the LaTeX content to a temporary file
            with open(tex_file, 'w') as f:
                f.write(tex)

            # Get path to temp LaTeX file
            temp_latex_filepath = os.path.join(temp_dir, tex_file)

            result = subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    f"-output-directory={temp_dir}",
                    tex_file,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )

            if result.returncode != 0:
                print(f"pdflatex error:\n{result.stderr}")
                return None

            # Move the PDF to the desired output location
            temp_pdf_filepath = os.path.join(temp_dir, pdf_file)
            if os.path.exists(temp_pdf_filepath):
                with open(temp_pdf_filepath, "rb") as f:
                    pdf_bytes = f.read()
                    # Close the file
                    f.close()
                return pdf_bytes
            else:
                print("PDF file was not generated.")
                return None

    except FileNotFoundError:
        raise RuntimeError("pdflatex not found. Make sure it is installed and in your PATH.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
