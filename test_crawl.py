
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

    def test_extract_page_data_one(self):
        input_url  = "https://crawler-test.com"
        input_html = '''
            <html>
                <body>
                    <h1>This is the first header</h1>
                    <p>This is text from first paragraph.</p>
                    <main>
                        <h2>This is the second header</h2>
                        <p>This is more text from second paragraph.</p>
                    </main>
                    <a href="/urltest">Go to Boot.dev</a>
                    <img src="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = {
            "url": "https://crawler-test.com",
            "heading": "This is the first header",
            "first_paragraph": "This is more text from second paragraph.",
            "outgoing_links": ["https://crawler-test.com/urltest"],
            "image_urls": ["https://crawler-test.com/logo.png"]
        }
        actual = extract_page_data(html, input_url)
        self.assertEqual(actual, expected)

    def test_extract_page_data_two(self):
        input_url  = "https://random-url.com"
        input_html = '''
            <html>
                <body>
                    <h1>This is the first header</h1>
                    <p>This is text from first paragraph.</p>
                    <a src="/urltest">Go to Boot.dev</a>
                    <img href="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = {
            "url": "https://random-url.com",
            "heading": "This is the first header",
            "first_paragraph": "This is text from first paragraph.",
            "outgoing_links": [],
            "image_urls": []
        }
        actual = extract_page_data(html, input_url)
        self.assertEqual(actual, expected)

    def test_extract_page_data_three(self):
        input_url  = "https://anothertesturl.com"
        input_html = '''
            <html>
                <body>
                    <main>
                        <h1>This is the first header</h1>
                        <p>This is text from first paragraph.</p>
                    </main>
                    <h2>This is the second header</h1>
                    <a href="/urltest">Go to Boot.dev</a>
                    <img href="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = {
            "url": "https://anothertesturl.com",
            "heading": "This is the first header",
            "first_paragraph": "This is text from first paragraph.",
            "outgoing_links": ["https://anothertesturl.com/urltest"],
            "image_urls": []
        }
        actual = extract_page_data(html, input_url)
        self.assertEqual(actual, expected)

    def test_extract_page_data_four(self):
        input_url  = "https://anothertesturl.com"
        input_html = '''
            <html>
                <body>
                    <main>
                        <h1>This is the first header</h1>
                        <p>This is text from first paragraph.</p>
                    </main>
                    <h2>This is the second header</h1>
                    <a src="/urltest">Go to Boot.dev</a>
                    <img src="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = {
            "url": "https://anothertesturl.com",
            "heading": "This is the first header",
            "first_paragraph": "This is text from first paragraph.",
            "outgoing_links": [],
            "image_urls": ["https://anothertesturl.com/logo.png"]
        }
        actual = extract_page_data(html, input_url)
        self.assertEqual(actual, expected)

    def test_extract_page_data_five(self):
        input_url  = "https://anothertesturl.com"
        input_html = '''
            <html>
                <body>
                    <main>
                        <p>This is text from first paragraph.</p>
                    </main>
                    <a href="/urltest">Go to Boot.dev</a>
                    <img src="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = {
            "url": "https://anothertesturl.com",
            "heading": "",
            "first_paragraph": "This is text from first paragraph.",
            "outgoing_links": ["https://anothertesturl.com/urltest"],
            "image_urls": ["https://anothertesturl.com/logo.png"]
        }
        actual = extract_page_data(html, input_url)
        self.assertEqual(actual, expected)

    def test_extract_page_data_six(self):
        input_url  = "https://anothertesturl.com"
        input_html = '''
            <html>
                <body>
                    <main>
                        <h2>This is the second header</h1>
                    </main>
                    <a href="/urltest">Go to Boot.dev</a>
                    <img src="/logo.png" alt="Boot.dev Logo" />
                </body>
            </html>
        '''
        html = BeautifulSoup(input_html, 'html.parser')
        expected = {
            "url": "https://anothertesturl.com",
            "heading": "This is the second header",
            "first_paragraph": "",
            "outgoing_links": ["https://anothertesturl.com/urltest"],
            "image_urls": ["https://anothertesturl.com/logo.png"]
        }
        actual = extract_page_data(html, input_url)
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
