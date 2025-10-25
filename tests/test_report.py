from datetime import datetime, timezone

from fashion_business_daily.articles import Article
from fashion_business_daily.report import build_markdown_digest


def test_build_markdown_digest_groups_articles() -> None:
    articles = [
        Article(
            source="Test Source",
            title="Brand appoints new creative director",
            url="https://example.com/creative",
            summary="A major creative director move.",
            published=datetime(2025, 10, 25, tzinfo=timezone.utc),
            categories=["Creative Director Moves"],
        ),
        Article(
            source="Test Source",
            title="Label launches sustainability initiative",
            url="https://example.com/sustain",
            summary="New sustainability strategy",
            published=datetime(2025, 10, 24, tzinfo=timezone.utc),
            categories=["Sustainability & Responsibility"],
        ),
    ]

    digest = build_markdown_digest(articles)

    assert "## Creative Director Moves" in digest
    assert "## Sustainability & Responsibility" in digest
    assert "Brand appoints new creative director" in digest
    assert "Label launches sustainability initiative" in digest
