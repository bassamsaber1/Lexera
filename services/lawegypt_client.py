from __future__ import annotations

from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lawegypt.net"


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


class LawEgyptClient:
    """Connector for lawegypt.net public pages (best-effort HTML parsing)."""

    def __init__(self, timeout: int = 20):
        self.timeout = timeout

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        response = requests.get(
            f"{BASE_URL}/",
            params={"s": query},
            timeout=self.timeout,
            headers={"User-Agent": "Lexera/1.0 (+research-assistant)"},
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        results: list[SearchResult] = []
        for heading in soup.select("h2 a, h3 a"):
            title = heading.get_text(strip=True)
            url = heading.get("href", "").strip()
            if not title or not url:
                continue
            container = heading.find_parent(["article", "div", "li"])
            snippet = ""
            if container:
                para = container.find("p")
                if para:
                    snippet = para.get_text(" ", strip=True)
            results.append(SearchResult(title=title, url=url, snippet=snippet))
            if len(results) >= limit:
                break

        return results

    def fetch_article_text(self, url: str) -> str:
        response = requests.get(
            url,
            timeout=self.timeout,
            headers={"User-Agent": "Lexera/1.0 (+research-assistant)"},
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        content_root = (
            soup.select_one("article")
            or soup.select_one(".entry-content")
            or soup.select_one("main")
            or soup.body
        )
        if content_root is None:
            return ""

        paragraphs = [p.get_text(" ", strip=True) for p in content_root.select("p")]
        text = "\n".join(line for line in paragraphs if line)
        return text[:20000]
