from pathlib import Path
import subprocess


def pdf_to_string(file_path, page):
    """
    Translates a page in a pdf file to text. Utilizes Xpdf.
    NOTICE: Because of the pdf format page index starts at 1.
    :param file_path: Path to the pdf file
    :param page: The page that will be translated
    :return: String containing the text in the pdf file
    """
    # Casts the page parameter to a string so integers can be used when calling the function
    page = str(page)

    # Program and it's arguments that get called here pdftotext from xpdf
    cmd = ["pdftotext", '-layout', '-enc', 'UTF-8', '-f', page, '-l', page, file_path, '-']

    # Opens a new process, connect to it's stdout, then read and return the output
    return subprocess.Popen(cmd,
                            encoding='utf-8',
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE).communicate()[0]


if __name__ == '__main__':
    pdf_file = Path('.') /'samples' / '0.pdf'
    test = str(pdf_file)
    print(pdf_to_string(test, 17))