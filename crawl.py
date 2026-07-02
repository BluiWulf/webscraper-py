
import re
import requests

from urllib.parse import *
from bs4 import BeautifulSoup, Tag
from pagedata import PageData

def normalize_url(input_url: str) -> str:
    url_Parts = tuple(urlparse(input_url))
    normal_url = ""
    for part in url_Parts[1:]:
        normal_url += part

    return normal_url.lower().rstrip("/")

def get_html(url: str) -> str:
    try:
        res = requests.get(url, headers = {"User-Agent": "BootCrawler/1.0"})
    except Exception as ex:
        raise Exception(ex)

    if res.status_code >= 400:
        res.raise_for_status()
    if "text/html" not in res.headers['Content-Type']:
        raise Exception("content-type is not text/html")

    return res.text

def get_heading_from_html(html: BeautifulSoup) -> str:
    header = html.find(re.compile('h\\d+'))
    return header.get_text(strip = True) if isinstance(header, Tag) else ""

def get_first_paragraph_from_html(html: BeautifulSoup) -> str:
    main = html.main
    if isinstance(main, Tag):
        paragraph = main.p
    else:
        paragraph = html.p

    return paragraph.get_text(strip = True) if isinstance(paragraph, Tag) else ""

def get_urls_from_html(html: BeautifulSoup, base_url: str):
    links = html.find_all("a", href = True)
    urls = []

    for link in links:
        try:
            urls.append(urljoin(base_url, link['href']))
        except Exception as ex:
            print(f'{str(ex)}: "{link['href']}"')

    return urls

def get_images_from_html(html: BeautifulSoup, base_url: str):
    images = html.find_all("img", src = True)
    urls = []

    for image in images:
        try:
            urls.append(urljoin(base_url, image['src']))
        except Exception as ex:
            print(f'{str(ex)}: "{image['href']}"')

    return urls

def extract_page_data(html: BeautifulSoup, page_url: str) -> PageData:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }

def crawl_page(base_url, current_url = None, page_data = None):
    if base_url not in current_url:
        return
    nrm_curr_url = normalize_url(current_url)
    if nrm_curr_url in page_data:
        return
    
    print(f'Fetching html data from: "{current_url}"')
    try:
        curr_html = get_html(current_url)
    except Exception as ex:
        raise Exception(f'error fetching HTML from "{current_url}": {str(ex)}')
    html_soup = BeautifulSoup(curr_html, 'html.parser')

    page_data[nrm_curr_url] = extract_page_data(html_soup, current_url)
    for sub_url in page_data[nrm_curr_url]["outgoing_links"]:
        crawl_page(base_url, sub_url, page_data)
