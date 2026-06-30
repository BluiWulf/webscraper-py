
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
    html = get_html(input_url)

    print(html)

if __name__ == "__main__":
    main()