
from crawl import *
from bs4 import BeautifulSoup, Tag

def main():
    input_url = "test.html"
    normal_url = normalize_url(input_url)

    with open(normal_url) as html_file:
        html = BeautifulSoup(html_file, 'html.parser')

    test_url = "https://crawler-test.com"
    urls = get_images_from_html(html, test_url)
    for url in urls:
        print(url)

if __name__ == "__main__":
    main()