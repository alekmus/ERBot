from bs4 import BeautifulSoup as bs
import sys
import ssl
from urllib.request import urlopen, Request
import requests
import PyPDF2
from pathlib import Path


class ERScraper:

    def _retrieve_pdf(self, press_release_url):
        """
        Retrieves a link to the earnings release pdf file from the press release.
        NOTICE: Does not currently support multiple reference links (if the ER is not the first one) or validate input
        in any way. These features are WIP until a working prototype is completed for current scope is completed.
        :param press_release_url: url address of the press release
        :return: a string containing the link
        """
        # TODO remember to return false if validations dictate it

        # TODO validate the address might be sufficient just to validate with TODO bellow
        url = press_release_url

        # Get the html for the ER press release to scrape the location of the pdf file
        # TODO validate type of press release and number of references.
        html = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), context=ssl.SSLContext())
        soup = bs(html, 'html.parser')

        # Find the word "liitteet" and pick the next element i.e the actual reference
        pdf_address = soup.find(text='Liitteet:').findNext('a')['href']
        pdf_file = requests.get(pdf_address)

        # Set up filepath for the temporary pdf file that needs to be downloaded
        root = Path('..')

        # Save the pdf to file
        with open(root / 'tmp' / '.tmp.pdf', 'wb') as f:
            f.write(pdf_file.content)

        # Returns true on successful download
        return True

    def _find_earnings_page(self, file_path):
        """
        Opens a pdf file based on the file_path parameter returns a table containing reported revenue, operating profit,
        pretax profit and profit per share
        :param file_path: filepath to the pdf file
        :return: pandas DataFrame
        """
        f = open(file_path, 'rb')
        file_reader = PyPDF2.PdfFileReader(f)

        # TODO Find a way to recognise the correct page
        for i in range(file_reader.getNumPages()):
            if self._validate(file_reader.getPage(i).extractText()):
                return i

    def _validate(self, input_string, mode='dumb'):
        # TODO return True if the earnings table is present
        return True


if __name__ == '__main__':
    scraper = ERScraper()
    # scraper._retrieve_pdf(sys.argv[1])
    pdf_path = Path('..') / 'tmp' / '.tmp.pdf'
    print(scraper._find_earnings_page(pdf_path))
