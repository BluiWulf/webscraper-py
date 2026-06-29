
import unittest

from crawl import *
from bs4 import BeautifulSoup, Tag

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    # This tests that the first header is detected and scraped correctly
    def test_get_heading_from_html_one(self):
        input_html = '''
            <html>
                <body>
                    <h1>This is the first header</h1>
                    <p>This is text from first paragraph.</p>
                    <h2>This is the second header</h2>
                    <p>This is more text from second paragraph.</p>
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = "This is the first header"
        actual = get_heading_from_html(html)
        self.assertEqual(actual, expected)

    # This tests that it finds the second header if no first header is present
    def test_get_heading_from_html_two(self):
        input_html = '''
            <html>
                <body>
                    <h2>This is the second header</h2>
                    <p>This is more text from second paragraph.</p>
                    <h3>This is the third header</h3>
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = "This is the second header"
        actual = get_heading_from_html(html)
        self.assertEqual(actual, expected)

    # This tests that it returns an empty string with no headers present
    def test_get_heading_from_html_three(self):
        input_html = '''
            <html>
                <body>
                    <p>This is more text from a random paragraph.</p>
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = ""
        actual = get_heading_from_html(html)
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_one(self):
        input_html = '''
            <html>
                <body>
                    <h1>This is the first header</h1>
                    <p>This is text from first paragraph.</p>
                    <main>
                        <h2>This is the second header</h2>
                        <p>This is more text from second paragraph.</p>
                    </main>
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = "This is more text from second paragraph."
        actual = get_first_paragraph_from_html(html)
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_two(self):
        input_html = '''
            <html>
                <body>
                    <h1>This is the first header</h1>
                    <p>This is text from first paragraph.</p>
                    <h2>This is the second header</h2>
                    <p>This is more text from second paragraph.</p>
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = "This is text from first paragraph."
        actual = get_first_paragraph_from_html(html)
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_one(self):
        input_html = '''
            <html>
                <body>
                    <a href="/urltest">Go to Boot.dev</a>
                    <img src="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = "https://crawler-test.com/urltest"
        links = get_urls_from_html(html, "https://crawler-test.com")
        actual = links[0]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_two(self):
        input_html = '''
            <html>
                <body>
                    <a src="/urltest">Go to Boot.dev</a>
                    <img src="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = []
        actual = get_urls_from_html(html, "https://crawler-test.com")
        self.assertEqual(actual, expected)

    def test_get_images_from_html_one(self):
        input_html = '''
            <html>
                <body>
                    <a href="/urltest">Go to Boot.dev</a>
                    <img src="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = "https://crawler-test.com/logo.png"
        images = get_images_from_html(html, "https://crawler-test.com")
        actual = images[0]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_two(self):
        input_html = '''
            <html>
                <body>
                    <a href="/urltest">Go to Boot.dev</a>
                    <img href="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = []
        actual = get_images_from_html(html, "https://crawler-test.com")
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
