"""
Data fetchers for financial news and stock prices.
All sources are 100% free — no API key, no signup required.

News: Google News RSS + Yahoo Finance RSS
Prices: Yahoo Finance Chart API
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


def fetch_news(ticker: str, company_name: str = "") -> list[dict]:
    """
    Fetch recent news headlines for a ticker from Google News + Yahoo Finance RSS.
    Returns list of dicts with 'title', 'source', 'date'.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    articles = []

    # Google News RSS
    query = f"{ticker} stock" if not company_name else f"{company_name} {ticker} stock"
    google_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    try:
        resp = requests.get(google_url, headers=headers, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            for item in root.findall(".//item"):
                title = item.find("title")
                pub = item.find("pubDate")
                source = item.find("source")
                if title is not None and title.text:
                    articles.append({
                        "title": title.text.strip(),
                        "source": source.text.strip() if source is not None and source.text else "Google News",
                        "date": pub.text.strip() if pub is not None and pub.text else "",
                        "feed": "google",
                    })
    except Exception:
        pass

    # Yahoo Finance RSS
    yahoo_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    try:
        resp = requests.get(yahoo_url, headers=headers, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            for item in root.findall(".//item"):
                title = item.find("title")
                pub = item.find("pubDate")
                if title is not None and title.text:
                    articles.append({
                        "title": title.text.strip(),
                        "source": "Yahoo Finance",
                        "date": pub.text.strip() if pub is not None and pub.text else "",
                        "feed": "yahoo",
                    })
    except Exception:
        pass

    # Deduplicate by title
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
    period: '5d', '1mo', '3mo', '6mo', '1y'
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

        # Clean nulls
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
            "dates": dates,
            "closes": prices,
            "current": prices[-1],
            "period_start": prices[0],
            "change": round(change, 2),
            "change_pct": change_pct,
            "ticker": ticker.upper(),
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
