
import asyncio
import aiohttp

from pagedata import PageData
from crawl import *
from urllib.parse import *

class AsyncCrawler():
    base_url: str                       # Starting URL
    base_domain: str                    # Domain name
    page_data: dict[str, PageData]      # Dictionary of page data, keyed by normalized URLs
    lock: asyncio.Lock                  # Async lock for task resources
    max_concurrency: int                # Number of requests limiter
    semaphore: asyncio.Semaphore        # Async task count manager
    session: aiohttp.ClientSession      # HTTP client session

    def __init__(self,
                 base_url:str,
                 base_domain: str,
                 page_data: dict[str, PageData],
                 lock: asyncio.Lock,
                 max_concurrency: int,
                 semaphore: asyncio.Semaphore,
                 session: aiohttp.ClientSession):
        self.base_url = base_url
        self.base_domain = base_domain
        self.page_data = page_data
        self.lock = lock
        self.max_concurrency = max_concurrency
        self.semaphore = semaphore
        self.session = session
        return self
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data.keys():
                return False
            self.page_data[normalized_url] = PageData("", "", "", [], [])
            return True

    async def get_html(self, url: str) -> str:
        try:
            async with self.session.get(url, headers = {"User-Agent": "BootCrawler/1.0"}) as res:
                if res.status_code >= 400:
                    res.raise_for_status()
                if "text/html" not in res.headers['Content-Type']:
                    raise Exception("content-type is not text/html")
                return await res.text()
        except Exception as ex:
            raise Exception(ex)

    async def crawl_page(self, current_url):
        parsed_url = urlparse(current_url)
        if not self.base_domain == parsed_url.netloc:
            return
        nrm_curr_url = normalize_url(current_url)
        if not await self.add_page_visit(nrm_curr_url):
            return
    
        print(f'Fetching html data from: "{current_url}"')
        try:
            async with self.semaphore:
                curr_html = self.get_html(current_url)
        except Exception as ex:
            raise Exception(f'error fetching HTML from "{current_url}": {str(ex)}')
        html_soup = BeautifulSoup(curr_html, 'html.parser')
        data = extract_page_data(html_soup, current_url)
        async with self.lock:
            self.page_data[nrm_curr_url] = data
        
        crawl_tasks = set()
        for sub_url in data["outgoing_links"]:
            crawl_tasks.add(asyncio.create_task(self.crawl_page(sub_url)))
        await asyncio.gather(*crawl_tasks)

    async def crawl(self) -> dict[str, PageData]:
        async with self.session:
            return await self.crawl_page(self.base_url)

async def crawl_site_async(base_url: str, max_tasks: int) -> dict[str, PageData]:
    parsed_url = urlparse(base_url)
    crawler: AsyncCrawler = AsyncCrawler(
        base_url,
        parsed_url.netloc,
        {},
        asyncio.Lock(),
        max_tasks,
        asyncio.Semaphore(max_tasks),
        aiohttp.ClientSession()
    )
    async with crawler:
        return await crawler.crawl()