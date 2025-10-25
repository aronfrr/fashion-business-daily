"""Data structures for Fashion Business Daily."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable, List, Optional, Set


@dataclass(frozen=True)
class Category:
    """Represents a tagged news category."""

    name: str
    keywords: Set[str]

    def match(self, text: str) -> bool:
        """Return ``True`` if the category keywords appear in ``text``."""

        lowered = text.lower()
        return any(keyword in lowered for keyword in self.keywords)


@dataclass
class Article:
    """Represents a single fashion business article."""

    source: str
    title: str
    url: str
    summary: str
    published: Optional[datetime]
    categories: List[str] = field(default_factory=list)

    def assign_categories(self, categories: Iterable[Category]) -> None:
        """Assign matching categories to this article."""

        text = f"{self.title}\n{self.summary}"
        matched: List[str] = []
        for category in categories:
            if category.match(text):
                matched.append(category.name)
        self.categories = matched

    @property
    def is_recent(self) -> bool:
        """Return ``True`` if the article was published in the last 72 hours."""

        if not self.published:
            return True
        return (datetime.now(timezone.utc) - self.published).total_seconds() <= 72 * 3600
