"""Generate a static website for GitHub Pages."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Dict, Iterable

from .articles import Article


def build_site_assets(articles: Iterable[Article], *, title: str = "Fashion Business Daily") -> Dict[str, str]:
    """Return a mapping of filename to content for a static site."""

    grouped = defaultdict(list)
    for article in articles:
        key = ", ".join(article.categories) if article.categories else "General"
        grouped[key].append(article)

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M %Z")

    sections: list[str] = []
    for category in sorted(grouped.keys()):
        section_lines = [f"<section class=\"category\" id=\"{escape(category.lower().replace(' ', '-'))}\">"]
        section_lines.append(f"  <h2>{escape(category)}</h2>")
        section_lines.append("  <ul class=\"stories\">")
        for article in grouped[category]:
            published = (
                article.published.strftime("%Y-%m-%d %H:%M %Z")
                if article.published
                else "Unknown"
            )
            section_lines.append(
                "    <li class=\"story\">"
                f"<a href=\"{escape(article.url)}\" target=\"_blank\" rel=\"noopener noreferrer\">"
                f"{escape(article.title)}</a>"
                f"<span class=\"meta\">{escape(article.source)} — {escape(published)}</span>"
                f"<p>{escape(article.summary.strip())}</p>"
                "    </li>"
            )
        section_lines.append("  </ul>")
        section_lines.append("</section>")
        sections.append("\n".join(section_lines))

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{escape(title)}</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <header class=\"hero\">
    <h1>{escape(title)}</h1>
    <p class=\"updated\">Last updated {escape(updated)}</p>
  </header>
  <main>
    {''.join(sections) if sections else '<p class="empty">No articles available.</p>'}
  </main>
  <footer>
    <p>Powered by trusted fashion business sources including Business of Fashion, WWD, Vanity Fair, Vogue Business, and The New York Times.</p>
  </footer>
</body>
</html>
"""

    css = """:root {\n  color-scheme: light dark;\n  font-family: 'Helvetica Neue', Arial, sans-serif;\n}\n\nbody {\n  margin: 0;\n  padding: 0;\n  background: #f8f9fb;\n  color: #202124;\n}\n\n.hero {\n  background: linear-gradient(135deg, #111827, #1f2937);\n  color: #f9fafb;\n  padding: 3rem 1.5rem;\n  text-align: center;\n}\n\n.hero h1 {\n  margin: 0;\n  font-size: clamp(2rem, 4vw, 3.25rem);\n}\n\n.hero .updated {\n  margin-top: 0.5rem;\n  font-size: 0.95rem;\n  opacity: 0.85;\n}\n\nmain {\n  max-width: 960px;\n  margin: 0 auto;\n  padding: 2rem 1.5rem 4rem;\n}\n\n.category {\n  margin-bottom: 2.5rem;\n}\n\n.category h2 {\n  font-size: 1.5rem;\n  border-bottom: 2px solid #1f2937;\n  padding-bottom: 0.5rem;\n  margin-bottom: 1rem;\n}\n\n.stories {\n  list-style: none;\n  padding: 0;\n  margin: 0;\n  display: grid;\n  gap: 1.5rem;\n}\n\n.story a {\n  font-weight: 600;\n  font-size: 1.1rem;\n  color: #1f2937;\n  text-decoration: none;\n}\n\n.story a:hover,\n.story a:focus {\n  text-decoration: underline;\n}\n\n.story .meta {\n  display: block;\n  font-size: 0.9rem;\n  margin-top: 0.35rem;\n  color: #4b5563;\n}\n\n.story p {\n  margin: 0.75rem 0 0;\n  line-height: 1.5;\n  color: #374151;\n}\n\nfooter {\n  background: #111827;\n  color: #f9fafb;\n  text-align: center;\n  padding: 1.25rem 1rem;\n  font-size: 0.9rem;\n}\n\n.empty {\n  text-align: center;\n  font-style: italic;\n  color: #4b5563;\n}\n"""

    return {"index.html": html, "styles.css": css}


def write_site(assets: Dict[str, str], output_dir: Path) -> Path:
    """Write static site assets to ``output_dir`` and return the directory."""

    output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in assets.items():
        (output_dir / name).write_text(content, encoding="utf-8")
    return output_dir
