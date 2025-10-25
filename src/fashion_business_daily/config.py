"""Project configuration helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - dependency optional for defaults
    yaml = None

from .articles import Category
from .sources import NYTimesTopStoriesSource, NewsSource, RSSNewsSource

DEFAULT_SOURCES = [
    RSSNewsSource("Business of Fashion", "https://www.businessoffashion.com/rss"),
    RSSNewsSource("WWD", "https://wwd.com/feed/"),
    RSSNewsSource("Vanity Fair Fashion", "https://www.vanityfair.com/feed/rss/fashion"),
    RSSNewsSource("Vogue Business", "https://www.voguebusiness.com/rss"),
    NYTimesTopStoriesSource("New York Times Fashion"),
]

DEFAULT_CATEGORIES: Dict[str, Iterable[str]] = {
    "Creative Director Moves": {
        "creative director",
        "artistic director",
        "creative lead",
        "chief creative officer",
        "design director",
    },
    "Executive & Leadership": {
        "chief executive",
        "ceo",
        "president",
        "chairman",
        "board appoints",
        "leadership",
    },
    "Acquisitions & Investments": {
        "acquires",
        "acquisition",
        "merger",
        "invests",
        "raises",
        "funding",
        "private equity",
    },
    "Marketing & Campaigns": {
        "marketing",
        "campaign",
        "ambassador",
        "brand campaign",
        "ad campaign",
        "collaboration",
        "capsule collection",
    },
    "Sustainability & Responsibility": {
        "sustainable",
        "sustainability",
        "esg",
        "responsibility",
        "climate",
        "carbon",
        "environmental",
    },
}

CONFIG_PATH = Path("config/sources.yaml")


def load_sources() -> List[NewsSource]:
    """Load news sources from ``config/sources.yaml`` if it exists."""

    if CONFIG_PATH.exists() and yaml is not None:
        with CONFIG_PATH.open("r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh) or {}
        return [
            _source_from_dict(source)
            for source in config.get("sources", [])
        ]
    return DEFAULT_SOURCES.copy()


def load_categories() -> List[Category]:
    """Return the default category configuration."""

    return [Category(name=name, keywords=set(keywords)) for name, keywords in DEFAULT_CATEGORIES.items()]


def _source_from_dict(payload: Dict[str, str]) -> NewsSource:
    kind = payload.get("type", "rss")
    name = payload["name"]
    if kind == "rss":
        return RSSNewsSource(name, payload["url"])
    if kind == "nyt_topstories":
        section = payload.get("section", "fashion")
        return NYTimesTopStoriesSource(name, section=section)
    raise ValueError(f"Unsupported source type: {kind}")
