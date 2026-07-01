
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

    input_url = sys.argv[1]
    normal_url = normalize_url(input_url)
    print(f'\nstarting crawl of: "{input_url}"\n')

    try:
        html = get_html(input_url)
    except Exception as ex:
        print(f'error fetching HTML from "{input_url}": {str(ex)}')
        sys.exit(1)

    print(html)
    sys.exit(0)

if __name__ == "__main__":
    main()