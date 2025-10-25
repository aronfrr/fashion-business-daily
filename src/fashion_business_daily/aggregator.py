"""Core news aggregation logic."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Iterable, List

from .articles import Article, Category
from .sources import NewsSource

LOGGER = logging.getLogger(__name__)


class NewsAggregator:
    """Fetch and categorise fashion business news from multiple sources."""

    def __init__(
        self,
        sources: Iterable[NewsSource],
        categories: Iterable[Category],
        *,
        max_items_per_source: int = 25,
    ) -> None:
        self.sources = list(sources)
        self.categories = list(categories)
        self.max_items_per_source = max_items_per_source

    def fetch(self) -> List[Article]:
        """Fetch articles from all configured sources."""

        all_articles: List[Article] = []
        for source in self.sources:
            try:
                articles = source.fetch(limit=self.max_items_per_source)
            except Exception as exc:  # pragma: no cover - defensive logging
                LOGGER.exception("Failed to fetch from %s: %s", source.name, exc)
                continue
            for article in articles:
                article.assign_categories(self.categories)
                if article.is_recent:
                    all_articles.append(article)
        # sort by published desc fallback to now
        all_articles.sort(
            key=lambda article: article.published or datetime.now(timezone.utc),
            reverse=True,
        )
        return all_articles
