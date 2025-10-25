"""Utilities for writing daily digests."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .articles import Article


def build_markdown_digest(articles: Iterable[Article]) -> str:
    """Return a markdown digest grouped by category."""

    grouped = defaultdict(list)
    for article in articles:
        key = ", ".join(article.categories) if article.categories else "General"
        grouped[key].append(article)

    lines = ["# Fashion Business Daily", ""]
    lines.append(
        f"_Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M %Z')}_"
    )
    lines.append("")

    for category in sorted(grouped.keys()):
        lines.append(f"## {category}")
        lines.append("")
        for article in grouped[category]:
            timestamp = (
                article.published.strftime("%Y-%m-%d %H:%M %Z")
                if article.published
                else "Unknown"
            )
            lines.append(
                f"- [{article.title}]({article.url}) — {article.source} ({timestamp})\n  "
                f"  {article.summary.strip()}"
            )
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def write_digest(markdown: str, output_dir: Path) -> Path:
    """Write the markdown digest to ``output_dir`` with a dated filename."""

    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"daily_digest_{datetime.now(timezone.utc).strftime('%Y_%m_%d')}.md"
    path = output_dir / filename
    path.write_text(markdown, encoding="utf-8")
    return path
