
import sys

from crawl import *
from bs4 import BeautifulSoup, Tag

def main():
    if len(sys.argv) < 2:
        print("\nno website provided\n")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("\ntoo many arguments provided\n")
        sys.exit(1)

    base_url = sys.argv[1]
    current_url = base_url
    crawler_data: dict[str, PageData] = {}

    print(f'\nStarting crawl of: "{base_url}"\n')
    try:
        crawl_page(base_url, current_url, crawler_data)
    except Exception as ex:
        print(f'\nwebcrawler error occurred: {str(ex)}\n')
        sys.exit(1)
    
    print(f"\nNumber of pages crawled and saved: {len(crawler_data.items())}\n")
    for page in crawler_data.values():
        print(f"\nData from {page["url"]}:\n{page}\n")
    sys.exit(0)

if __name__ == "__main__":
    main()