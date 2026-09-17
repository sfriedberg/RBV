"""Secondary research layer for dialpha.

Pulls AlphaSense (or SEC EDGAR filings if no API key is set) and correlates
deal-level patterns with public-market signals.

Data land on disk in ``~/.dialpha/cache/`` — nothing leaves the machine.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

from .engine import KNOWN_PATTERNS, score_deal

# ---------------------------------------------------------------------------
# Config / cache (all local)
# ---------------------------------------------------------------------------

DOT_DIR = Path.home() / ".dialpha"       # ~/.dialpha/
CACHE_DIR = DOT_DIR / "cache"
CONFIG = DOT_DIR / "config.json"

DOT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

DEFAULT_CONFIG: Dict[str, Any] = {
    "alphasense_api_key": None,          # null → falls back to SEC EDGAR
    "ticker_whitelist": [],              # empty list = score everything
    "auto_research_on_score_gt": 0.50,   # fetch research if composite >= this
}


def config() -> Dict[str, Any]:
    """Return user configuration (defaults if file missing)."""
    if not CONFIG.exists():
        return dict(DEFAULT_CONFIG)
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def save_config(cfg: Dict[str, Any]) -> None:
    CONFIG.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def _cache_key(ticker: str) -> str:
    return hashlib.sha256(ticker.lower().encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------
# SEC EDGAR lightweight fetcher (no API key needed)
# ---------------------------------------------------------------------------

def fetch_edgar_filing(
    ticker: str,
    form: str = "10-K",
    days_back: int = 365,
) -> Dict[str, Any]:
    """Fetch the most recent EDGAR filing (default 10-K) for a public company.

    Caches to ``~/.dialpha/cache/`` for 24 h. Never raises — returns a dict
    with ``{"body", "source_url"}`` plus ``error``/``warning`` keys on failure.
    """
    cache_path = CACHE_DIR / f"{_cache_key(ticker)}_{form}.json"

    if cache_path.exists():
        age_hours = (time.time() - cache_path.stat().st_mtime) / 3600.0
        if age_hours < 24:
            return json.loads(cache_path.read_text(encoding="utf-8"))

    base = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "ticker": ticker,
        "type": form.replace("-", ""),
        "count": 1,
        "dateb": (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d"),
    }
    try:
        resp = requests.get(base, params=params, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        filing_link = soup.find(
            "a", href=True,
            string=lambda s: s and form in s and ".htm" in s,
        )
        if not filing_link:
            return {
                "body": "", "source_url": "",
                "warning": f"No {form} found for {ticker}",
            }
        url = "https://www.sec.gov" + filing_link["href"]
        resp2 = requests.get(url, timeout=30)
        resp2.raise_for_status()
        body = BeautifulSoup(resp2.text, "html.parser").get_text(
            separator="\n", strip=True,
        )
        payload = {
            "body": body,
            "source_url": url,
            "cached_at": datetime.now(timezone.utc).isoformat(),
        }
        cache_path.write_text(json.dumps(payload), encoding="utf-8")
        return payload
    except Exception as exc:
        if cache_path.exists():
            return json.loads(cache_path.read_text(encoding="utf-8"))
        return {"body": "", "source_url": "", "error": str(exc)}


# ---------------------------------------------------------------------------
# AlphaSense wrapper (optional — key in ~/.dialpha/config.json)
# ---------------------------------------------------------------------------

def fetch_alphasense(ticker: str, query: str = "") -> Dict[str, Any]:
    """Query AlphaSense when an API key is present; otherwise stub out.

    With no key configured this returns a stable empty result so the
    pipeline continues on SEC EDGAR data alone.
    """
    api_key = config().get("alphasense_api_key")
    if not api_key:
        return {
            "body": "", "source": "alphasense-stub",
            "note": "No API key set; using SEC EDGAR fallback.",
        }

    # Placeholder for a real integration: POST to AlphaSense with bearer
    # api_key and a search query built from the extracted patterns.
    return {
        "body": "", "source": "alphasense-stub",
        "note": f"Key present but integration stubbed → query={query!r}",
    }


# ---------------------------------------------------------------------------
# ResearchEngine (public API for this module)
# ---------------------------------------------------------------------------

class ResearchEngine:
    """Fetch secondary evidence, score it against deal patterns, rank."""

    def __init__(self) -> None:
        self._known_patterns: Dict[str, Any] | None = None

    @property
    def patterns(self) -> Dict[str, Any]:
        if self._known_patterns is None:
            self._known_patterns = KNOWN_PATTERNS
        return self._known_patterns

    def fetch_and_score(
        self,
        ticker: str,
        seed_text: str = "",
    ) -> List[Dict[str, Any]]:
        """Fetch EDGAR + AlphaSense for *ticker*, then score the best available text."""
        es_result = fetch_edgar_filing(ticker)
        as_result = fetch_alphasense(ticker, query=seed_text)

        text_to_score = seed_text or es_result.get("body", "")
        if not text_to_score:
            text_to_score = f"Ticker {ticker} has no public data yet."

        deal_result = score_deal(text_to_score)
        return [
            dict(
                deal_result,
                ticker=ticker,
                research={"source_url": es_result.get("source_url", ""),
                          "warning": es_result.get("warning", ""),
                          "error": es_result.get("error", "")},
                alphasense=as_result,
            )
        ]

    def batch_research(
        self,
        tickers: List[str],
        seed_text_template: str = "",
    ) -> List[Dict[str, Any]]:
        """Fetch + score for a list of tickers, ranked by composite score."""
        all_results: List[Dict[str, Any]] = []
        for t in tickers:
            all_results.extend(self.fetch_and_score(t, seed_text_template))
        all_results.sort(key=lambda r: r["composite_score"], reverse=True)
        return all_results
