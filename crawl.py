
from urllib.parse import urlparse

def normalize_url(input_url: str) -> str:
    url_Parts = tuple(urlparse(input_url))
    normal_url = ""
    for part in url_Parts[1:]:
        normal_url += part

    return normal_url.lower().rstrip("/")
