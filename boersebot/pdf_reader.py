from pathlib import Path
import subprocess


def pdf_to_string(file_path):
    """
    Converts a pdf file to text. Utilizes Xpdf.
    :param file_path: Path to the pdf file
    :return: String containing the text in the pdf file
    """

    return subprocess.run(["pdftotext", file_path, "-"]).stdout


if __name__ == '__main__':
    pdf_file = Path('.') / 'modelbuilder'/'samples' / '0.pdf'
    test = str(pdf_file)
    print(pdf_to_string(test))