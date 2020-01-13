import subprocess


def pdf_page_to_string(file_path, page):
    """
    Translates a page in a pdf file to text. Utilizes Xpdf.
    NOTICE: Because of the pdf format page index starts at 1.
    :param file_path: Path to the pdf file
    :param page: The page that will be translated
    :return: String containing the text on the give page in the pdf file
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


def pdf_to_string(file_path):
    """
    Translates the whole pdf file to text. Utilizes Xpdf.
    NOTICE: Because of the pdf format page index starts at 1.
    :param file_path: Path to the pdf file
    :return: String containing the text in the pdf file
    """

    # Program and it's arguments that get called here pdftotext from xpdf
    cmd = ["pdftotext", '-layout', '-enc', 'UTF-8', file_path, '-']

    # Opens a new process, connect to it's stdout, then read and return the output
    return subprocess.Popen(cmd,
                            encoding='utf-8',
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE).communicate()[0]


def pdf_to_pages(pdf_string):
    """
    Splits a string on feedforward character and excludes the last split.
    :param pdf_string: String representation of a pdf file.
    :return: List of strings
    """
    return pdf_string.split('\f')[:-1]


if __name__ == '__main__':
    sample = (pdf_to_string("samples/0.pdf"))
    pages = pdf_to_pages(sample)
    print(pages[-1])