"""Fashion Business Daily news aggregation package."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = ["Article", "Category", "NewsAggregator", "load_sources", "load_categories"]

if TYPE_CHECKING:  # pragma: no cover - import-time hints only
    from .aggregator import NewsAggregator
    from .articles import Article, Category
    from .config import load_categories, load_sources


def __getattr__(name: str) -> Any:  # pragma: no cover - simple proxy
    if name in {"Article", "Category"}:
        module = import_module(".articles", __name__)
        return getattr(module, name)
    if name == "NewsAggregator":
        module = import_module(".aggregator", __name__)
        return getattr(module, name)
    if name in {"load_sources", "load_categories"}:
        module = import_module(".config", __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
