"""
Data fetchers for financial news and stock prices.
All sources are 100% free — no API key, no signup required.

News: Google News RSS + Yahoo Finance RSS
      Now extracts <description> tags (article summaries, ~100-200 words)
      in addition to titles, giving the LM lexicon far more signal to work with.

Prices: Yahoo Finance Chart API
"""

import requests
import xml.etree.ElementTree as ET
import re
from datetime import datetime


def _clean_html(text: str) -> str:
    """Strip HTML tags from RSS description fields."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_news(ticker: str, company_name: str = "") -> list[dict]:
    """
    Fetch recent news for a ticker from Google News + Yahoo Finance RSS.
    Each article returns 'title', 'description', 'text' (title + description),
    'source', 'date'.

    'text' is what gets passed to analyze_sentiment — it combines the title
    and the article summary/description for a much richer signal than
    headlines alone.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    articles = []

    # --- Google News RSS ---
    query = f"{ticker} stock" if not company_name else f"{company_name} {ticker} stock"
    google_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    try:
        resp = requests.get(google_url, headers=headers, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            for item in root.findall(".//item"):
                title_el = item.find("title")
                desc_el   = item.find("description")
                pub_el    = item.find("pubDate")
                source_el = item.find("source")

                title = title_el.text.strip() if title_el is not None and title_el.text else ""
                desc  = _clean_html(desc_el.text) if desc_el is not None and desc_el.text else ""

                if title:
                    articles.append({
                        "title":       title,
                        "description": desc,
                        "text":        f"{title}. {desc}".strip(),
                        "source":      source_el.text.strip() if source_el is not None and source_el.text else "Google News",
                        "date":        pub_el.text.strip() if pub_el is not None and pub_el.text else "",
                        "feed":        "google",
                    })
    except Exception:
        pass

    # --- Yahoo Finance RSS ---
    yahoo_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    try:
        resp = requests.get(yahoo_url, headers=headers, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            for item in root.findall(".//item"):
                title_el = item.find("title")
                desc_el   = item.find("description")
                pub_el    = item.find("pubDate")

                title = title_el.text.strip() if title_el is not None and title_el.text else ""
                desc  = _clean_html(desc_el.text) if desc_el is not None and desc_el.text else ""

                if title:
                    articles.append({
                        "title":       title,
                        "description": desc,
                        "text":        f"{title}. {desc}".strip(),
                        "source":      "Yahoo Finance",
                        "date":        pub_el.text.strip() if pub_el is not None and pub_el.text else "",
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
