
import asyncio
import aiohttp

from pagedata import PageData
from crawl import *
from urllib.parse import *
from types import TracebackType

class AsyncCrawler():
    base_url: str                           # Starting URL
    base_domain: str                        # Domain name
    page_data: dict[str, PageData]          # Dictionary of page data, keyed by normalized URLs
    lock: asyncio.Lock                      # Async lock for task resources
    max_concurrency: int                    # Number of requests limiter
    semaphore: asyncio.Semaphore            # Async task count manager
    session: aiohttp.ClientSession | None   # HTTP client session

    def __init__(self, base_url:str):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 3
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
    
    async def __aenter__(self) -> "AsyncCrawler":
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> None:
        assert self.session is not None
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data.keys():
                return False
            return True

    async def get_html(self, url: str) -> str:
        try:
            assert self.session is not None
            async with self.session.get(url, headers = {"User-Agent": "BootCrawler/1.0"}) as res:
                if res.status >= 400:
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
                curr_html = await self.get_html(current_url)
        except Exception as ex:
            raise Exception(f'error fetching HTML from "{current_url}": {str(ex)}')
        html_soup = BeautifulSoup(curr_html, 'html.parser')
        data = extract_page_data(html_soup, current_url)
        async with self.lock:
            self.page_data[nrm_curr_url] = data
        
        crawl_tasks: list[asyncio.Task[None]] = []
        for sub_url in data["outgoing_links"]:
            crawl_tasks.append(asyncio.create_task(self.crawl_page(sub_url)))
        if crawl_tasks:
            await asyncio.gather(*crawl_tasks)

    async def crawl(self) -> dict[str, PageData]:
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url: str) -> dict[str, PageData]:
    crawler: AsyncCrawler = AsyncCrawler(base_url)
    async with crawler:
        return await crawler.crawl()