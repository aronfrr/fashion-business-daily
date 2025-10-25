"""Command line interface for Fashion Business Daily."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .aggregator import NewsAggregator
from .config import load_categories, load_sources
from .report import build_markdown_digest, write_digest

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fashion Business Daily aggregator")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data"),
        help="Directory to store generated daily digest files (default: data)",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=20,
        help="Maximum number of stories to fetch from each source",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    LOGGER.info("Fetching news from configured sources…")
    aggregator = NewsAggregator(
        sources=load_sources(),
        categories=load_categories(),
        max_items_per_source=args.max_items,
    )
    articles = aggregator.fetch()
    LOGGER.info("Fetched %d articles", len(articles))

    digest = build_markdown_digest(articles)
    output_path = write_digest(digest, args.output)
    LOGGER.info("Digest written to %s", output_path)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
