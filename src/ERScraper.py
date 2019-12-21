from bs4 import BeautifulSoup as bs
import sys
import ssl
from urllib.request import urlopen, Request
import  requests
import PyPDF2
from pathlib import Path

class ERScraper:

    def retrieve_pdf(self, press_release_url):
        """
        Retrieves a link to the earnings release pdf file from the press release.
        NOTICE: Does not currently support multiple reference links (if the ER is not the first one) or validate input
        in any way. These features are WIP until a working prototype is completed for current scope is completed.
        :param press_release_url: url address of the press release
        :return: a string containing the link
        """
        url = press_release_url
        html = urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), context=ssl.SSLContext())
        soup = bs(html, 'html.parser')
        pdf_address = soup.find(text='Liitteet:').findNext('a')['href']
        pdf_file = requests.get(pdf_address)
        root = Path('..')
        with open(root/'tmp'/'.tmp.pdf', 'wb') as f:
            f.write(pdf_file.content)
        return True


if __name__ == '__main__':
    scraper = ERScraper()
    print(scraper.retrieve_pdf(sys.argv[1]))
