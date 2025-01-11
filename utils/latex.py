import uuid
import os

def tex_to_pdf(tex, pdflatex_bin_loc):
    file_name = str(uuid.uuid4())
    tex_file = f'{file_name}.tex'
    pdf_file = f'{file_name}.pdf'

    with open(tex_file, 'w') as f:
        f.write(tex)

    os.system(f'{pdflatex_bin_loc} {file_name}')

    return pdf_file