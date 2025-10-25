from datetime import datetime, timezone

from fashion_business_daily.articles import Article
from fashion_business_daily.site import build_site_assets


def test_site_contains_categories_and_articles():
    articles = [
        Article(
            title="Creative Director moves",
            url="https://example.com/director",
            source="Business of Fashion",
            summary="Big change in leadership.",
            categories=("Creative Leadership",),
            published=datetime(2024, 5, 1, tzinfo=timezone.utc),
        ),
        Article(
            title="Marketing push",
            url="https://example.com/marketing",
            source="WWD",
            summary="New campaign launched.",
            categories=("Marketing",),
            published=datetime(2024, 5, 2, tzinfo=timezone.utc),
        ),
    ]

    assets = build_site_assets(articles)
    html = assets["index.html"]

    assert "Creative Leadership" in html
    assert "Marketing" in html
    assert "https://example.com/director" in html
    assert "https://example.com/marketing" in html
