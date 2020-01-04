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


def pdf_string_to_pages(pdf_string):
    """
    Breaks a pdf that has been converted to text into a list containing strings of each page
    :param pdf_string:
    :return:
    """
    # TODO documentation and pretty much everything else


if __name__ == '__main__':
    print(pdf_to_string("samples/0.pdf"))