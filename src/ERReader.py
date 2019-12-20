from bs4 import BeautifulSoup as bs
import pandas as pd
import sys
import ssl
from urllib.request import urlopen, Request


def retrieve_pdf_link(press_release_url):
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
    return soup.find(text='Liitteet:').findNext('a')['href']

print(retrieve_pdf_link(sys.argv[1]))
