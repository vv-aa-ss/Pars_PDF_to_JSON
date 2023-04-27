import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def get_pdf(url):
    # Our Folder
    folder_location = r'PDF'
    if not os.path.exists(folder_location):os.mkdir(folder_location)
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")
    number_file = 1
    for link in soup.select("a[href$='.pdf']"):

        filename = os.path.join(folder_location, link['href'].split('/')[-1])
        print(f"[INFO] Download ->> {link['href']}   Status:", end="")
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url, link['href'])).content)
            print("Ok")
