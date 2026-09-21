import uuid
import subprocess
import tempfile
import os
import re
import sys
import time


def _log(msg):
    print(f"[pdf] {msg}", file=sys.stderr, flush=True)


_ERROR_PATTERN = re.compile(r"^!|error|not found|undefined|fatal|emergency|no file", re.IGNORECASE)


def _log_pdflatex_output(output, max_error_lines=60, tail_lines=25):
    lines = output.splitlines()
    errors = [line for line in lines if _ERROR_PATTERN.search(line)]
    _log(f"----- pdflatex errors ({len(errors)} matching lines) -----")
    for line in errors[-max_error_lines:]:
        _log(line)
    _log(f"----- last {tail_lines} lines -----")
    for line in lines[-tail_lines:]:
        _log(line)
    _log("----- end pdflatex output -----")


def latex_to_pdf(tex):
    """
    Converts a LaTeX file to a PDF using pdflatex.

    Args:
        tex: Contents of the LaTeX file as a string.

    Returns:
        PDF bytes on success.
        Raises FileNotFoundError if pdflatex does not exist.
        Raises RuntimeError if pdflatex is not installed or if there is a problem during compilation.
    """
    file_name = str(uuid.uuid4())
    tex_file = f'{file_name}.tex'
    pdf_file = f'{file_name}.pdf'

    _log(f"start: type={type(tex).__name__}, len={len(tex) if hasattr(tex, '__len__') else '?'}")

    try:
        # Use a temporary directory to avoid cluttering the current directory
        with tempfile.TemporaryDirectory("tmp") as temp_dir:
            # Get path to temp LaTeX file
            temp_latex_filepath = os.path.join(temp_dir, tex_file)

            # Write the LaTeX content to a temporary file
            with open(temp_latex_filepath, 'w') as f:
                f.write(tex)

            t_start = time.perf_counter()
            result = subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    f"-output-directory={temp_dir}",
                    temp_latex_filepath,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            elapsed = time.perf_counter() - t_start
            output = result.stdout or ""

            if result.returncode != 0:
                _log(f"pdflatex FAILED after {elapsed:.1f}s (rc={result.returncode})")
                _log_pdflatex_output(output)
                raise RuntimeError("pdflatex failed to compile the document. See server logs for details.")

            _log(f"pdflatex ok in {elapsed:.1f}s")

            # Move the PDF to the desired output location
            temp_pdf_filepath = os.path.join(temp_dir, pdf_file)
            if os.path.exists(temp_pdf_filepath):
                with open(temp_pdf_filepath, "rb") as f:
                    return f.read()

            _log("pdflatex reported success but no PDF was produced")
            raise RuntimeError("pdflatex did not produce a PDF file.")

    except FileNotFoundError:
        _log("FileNotFoundError in latex_to_pdf (pdflatex missing, or temp dir unavailable)")
        raise RuntimeError("pdflatex not found. Make sure it is installed and in your PATH.")
    except Exception as e:
        _log(f"unexpected error before/around pdflatex: {type(e).__name__}: {e}")
        _log(f"tex content ({type(tex).__name__}): {tex!r}")
        raise
