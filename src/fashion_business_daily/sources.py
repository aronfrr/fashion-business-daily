"""Definitions of supported news sources."""

from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable, List, Optional

import requests

from .articles import Article

USER_AGENT = (
    "FashionBusinessDaily/0.1 (+https://github.com/example/fashion-business-daily)"
)


class NewsSource(ABC):
    """Abstract base class for news sources."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def fetch(self, *, limit: int) -> List[Article]:
        """Return a list of articles from the source."""


class RSSNewsSource(NewsSource):
    """Fetch articles from an RSS or Atom feed."""

    def __init__(self, name: str, url: str) -> None:
        super().__init__(name)
        self.url = url

    def fetch(self, *, limit: int) -> List[Article]:  # noqa: D401 - inherited
        response = requests.get(self.url, headers={"User-Agent": USER_AGENT}, timeout=30)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        items: Iterable[ET.Element]
        if root.tag.endswith("feed"):
            items = root.findall("{http://www.w3.org/2005/Atom}entry")
            return [
                _article_from_atom(self.name, entry) for entry in list(items)[:limit]
            ]
        channel = root.find("channel")
        if channel is None:
            items = root.findall("item")
        else:
            items = channel.findall("item")
        return [
            _article_from_rss(self.name, item) for item in list(items)[:limit]
        ]


class NYTimesTopStoriesSource(NewsSource):
    """Fetch fashion stories from The New York Times Top Stories API."""

    def __init__(self, name: str, section: str = "fashion") -> None:
        super().__init__(name)
        self.section = section

    def fetch(self, *, limit: int) -> List[Article]:  # noqa: D401 - inherited
        api_key = os.environ.get("NYTIMES_API_KEY")
        if not api_key:
            raise RuntimeError(
                "NYTIMES_API_KEY environment variable is required for New York Times access."
            )
        url = (
            f"https://api.nytimes.com/svc/topstories/v2/{self.section}.json?api-key={api_key}"
        )
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        results = payload.get("results", [])
        articles: List[Article] = []
        for item in results[:limit]:
            published = _parse_datetime(item.get("published_date"))
            article = Article(
                source=self.name,
                title=item.get("title", "Untitled"),
                url=item.get("url", ""),
                summary=item.get("abstract", ""),
                published=published,
            )
            articles.append(article)
        return articles


def _article_from_rss(source: str, item: ET.Element) -> Article:
    title = item.findtext("title") or "Untitled"
    summary = item.findtext("description") or item.findtext("summary") or ""
    summary = _strip_html(summary)
    url = item.findtext("link") or ""
    published = _parse_datetime(item.findtext("pubDate"))
    return Article(source=source, title=title.strip(), url=url.strip(), summary=summary.strip(), published=published)


def _article_from_atom(source: str, entry: ET.Element) -> Article:
    ns = "{http://www.w3.org/2005/Atom}"
    title = entry.findtext(f"{ns}title") or "Untitled"
    summary = entry.findtext(f"{ns}summary") or entry.findtext(f"{ns}content") or ""
    summary = _strip_html(summary)
    url = ""
    link_el = entry.find(f"{ns}link[@rel='alternate']") or entry.find(f"{ns}link")
    if link_el is not None:
        url = link_el.get("href", "")
    published = _parse_datetime(entry.findtext(f"{ns}updated")) or _parse_datetime(
        entry.findtext(f"{ns}published")
    )
    return Article(source=source, title=title.strip(), url=url.strip(), summary=summary.strip(), published=published)


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (TypeError, ValueError):
        try:
            return datetime.fromisoformat(value).astimezone(timezone.utc)
        except ValueError:
            return None


TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(value: str) -> str:
    """Remove simple HTML tags from feed summaries."""

    if not value:
        return ""
    return TAG_RE.sub("", value).strip()
