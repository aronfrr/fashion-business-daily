# Fashion Business Daily

Fashion Business Daily is a lightweight command-line tool that curates the latest
fashion business headlines every morning. It focuses on news around creative
leadership moves, acquisitions, investments, marketing campaigns, and broader
industry responsibility topics.

## Features

- Pulls stories from reliable publications such as Business of Fashion, WWD,
  Vanity Fair, Vogue Business, and The New York Times fashion desk.
- Classifies headlines into business-focused categories (creative director
  movements, leadership changes, marketing initiatives, sustainability, etc.).
- Generates a Markdown digest grouped by category so you can scan the morning's
  most important developments in minutes.

## Getting started

1. Create and activate a Python 3.10+ environment.
2. Install the dependencies:

   ```bash
   pip install .
   ```

3. Export your New York Times API key so the app can pull fashion desk top
   stories:

   ```bash
   export NYTIMES_API_KEY="your-api-key"
   ```

   You can request an API key for free from the [New York Times developer
   portal](https://developer.nytimes.com/).

4. Run the aggregator:

   ```bash
   fashion-business-daily --output data
   ```

   A dated Markdown file (for example `daily_digest_2025_10_25.md`) will be
   generated inside the chosen output directory.

   To publish a live dashboard on GitHub Pages, generate the static site assets
   into a `docs/` folder (the location GitHub Pages can serve from):

   ```bash
   fashion-business-daily --output data --site-output docs
   ```

   Commit the `docs/` directory, then enable Pages in your repository settings
   and choose the `main` branch with the `/docs` folder.

   For fully automated updates, add a scheduled GitHub Actions workflow that
   runs the same command, commits the refreshed digest and site, and pushes the
   changes back to your repository.

## Customising sources

The tool ships with a default list of trusted publications. If you want to add
or remove feeds, copy `config/sources.yaml`, uncomment the `sources` block, and
list your own entries. Supported types are:

- `rss` for RSS/Atom feeds (requires `url`).
- `nyt_topstories` for New York Times sections (requires an API key and optional
  `section`).

```yaml
sources:
  - name: "Business of Fashion"
    type: "rss"
    url: "https://www.businessoffashion.com/rss"
  - name: "New York Times Fashion"
    type: "nyt_topstories"
    section: "fashion"
```

## Automating the daily refresh

Schedule the command to run every morning using cron (macOS/Linux example):

```cron
0 6 * * * /path/to/venv/bin/fashion-business-daily --output /path/to/fashion-business-daily/data
```

For Windows, create a Task Scheduler job that runs the same command each day.

## Troubleshooting

- Some publishers restrict RSS access. Ensure your network allows outbound HTTPS
  requests and that the source supports RSS.
- If you are behind a proxy, set the `HTTP_PROXY`/`HTTPS_PROXY` environment
  variables before running the command.
- For The New York Times, double-check that `NYTIMES_API_KEY` is set and valid.

## License

This project is released under the MIT License.
