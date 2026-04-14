"""
Data fetchers for financial news and stock prices.
All sources are 100% free — no API key, no signup required.

News: Google News RSS + Yahoo Finance RSS
      - Google News: uses after:YYYY-MM-DD operator to filter by period
      - Yahoo Finance: filters by parsing pubDate field
      - Both now respect the selected time period (5d, 1mo, 3mo)
      - Extracts <description> tags for richer sentiment signal

Prices: Yahoo Finance Chart API
"""

import requests
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean_html(text: str) -> str:
    """Strip HTML tags from RSS description fields."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _period_to_days(period: str) -> int:
    return {"5d": 5, "1mo": 30, "3mo": 90}.get(period, 30)


def _parse_pub_date(date_str: str) -> datetime | None:
    """Parse RSS pubDate string to datetime. Returns None on failure."""
    if not date_str:
        return None
    try:
        return parsedate_to_datetime(date_str).replace(tzinfo=None)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# News fetcher
# ---------------------------------------------------------------------------

def fetch_news(ticker: str, company_name: str = "", period: str = "1mo") -> list[dict]:
    """
    Fetch recent news for a ticker from Google News + Yahoo Finance RSS.
    Filters articles to only those published within the selected period.

    Each article returns:
      'title', 'description', 'text' (title + description), 'source', 'date'

    'text' is passed to analyze_sentiment for richer signal than titles alone.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    articles = []

    days = _period_to_days(period)
    cutoff = datetime.now() - timedelta(days=days)
    after_date = cutoff.strftime("%Y-%m-%d")

    # --- Google News RSS (supports after: date operator) ---
    base_query = f"{company_name} {ticker} stock" if company_name else f"{ticker} stock"
    query = f"{base_query} after:{after_date}"
    google_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

    try:
        resp = requests.get(google_url, headers=headers, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            for item in root.findall(".//item"):
                title_el  = item.find("title")
                desc_el   = item.find("description")
                pub_el    = item.find("pubDate")
                source_el = item.find("source")

                title    = title_el.text.strip() if title_el is not None and title_el.text else ""
                desc     = _clean_html(desc_el.text) if desc_el is not None and desc_el.text else ""
                pub_raw  = pub_el.text.strip() if pub_el is not None and pub_el.text else ""
                pub_date = _parse_pub_date(pub_raw)

                # Secondary date filter — belt and braces in case Google returns
                # older articles despite the after: operator
                if pub_date and pub_date < cutoff:
                    continue

                if title:
                    articles.append({
                        "title":       title,
                        "description": desc,
                        "text":        f"{title}. {desc}".strip(),
                        "source":      source_el.text.strip() if source_el is not None and source_el.text else "Google News",
                        "date":        pub_raw,
                        "feed":        "google",
                    })
    except Exception:
        pass

    # --- Yahoo Finance RSS (no native date filter — filter by pubDate) ---
    yahoo_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"

    try:
        resp = requests.get(yahoo_url, headers=headers, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            for item in root.findall(".//item"):
                title_el = item.find("title")
                desc_el  = item.find("description")
                pub_el   = item.find("pubDate")

                title    = title_el.text.strip() if title_el is not None and title_el.text else ""
                desc     = _clean_html(desc_el.text) if desc_el is not None and desc_el.text else ""
                pub_raw  = pub_el.text.strip() if pub_el is not None and pub_el.text else ""
                pub_date = _parse_pub_date(pub_raw)

                # Filter out articles older than the selected period
                if pub_date and pub_date < cutoff:
                    continue

                if title:
                    articles.append({
                        "title":       title,
                        "description": desc,
                        "text":        f"{title}. {desc}".strip(),
                        "source":      "Yahoo Finance",
                        "date":        pub_raw,
                        "feed":        "yahoo",
                    })
    except Exception:
        pass

    # --- Deduplicate by title ---
    seen = set()
    unique = []
    for a in articles:
        key = a["title"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(a)

    return unique


# ---------------------------------------------------------------------------
# Price fetcher
# ---------------------------------------------------------------------------

def fetch_stock_prices(ticker: str, period: str = "1mo") -> dict | None:
    """
    Fetch historical stock prices from Yahoo Finance.
    period: '5d', '1mo', '3mo'
    Returns dict with 'dates', 'closes', 'change_pct', 'current', 'period_start'.
    """
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker.upper()}"
    params = {"interval": "1d", "range": period}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes = result["indicators"]["quote"][0]["close"]

        dates = []
        prices = []
        for ts, c in zip(timestamps, closes):
            if c is not None:
                dates.append(datetime.fromtimestamp(ts).strftime("%Y-%m-%d"))
                prices.append(round(c, 2))

        if len(prices) < 2:
            return None

        change = prices[-1] - prices[0]
        change_pct = round((change / prices[0]) * 100, 2)

        return {
            "dates":        dates,
            "closes":       prices,
            "current":      prices[-1],
            "period_start": prices[0],
            "change":       round(change, 2),
            "change_pct":   change_pct,
            "ticker":       ticker.upper(),
        }
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Company name fetcher
# ---------------------------------------------------------------------------

def fetch_company_name(ticker: str) -> str:
    """Fetch company name from Yahoo Finance."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker.upper()}"
    params = {"interval": "1d", "range": "1d"}
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        meta = data["chart"]["result"][0]["meta"]
        name = meta.get("longName") or meta.get("shortName") or ticker.upper()
        return name
    except Exception:
        return ticker.upper()
