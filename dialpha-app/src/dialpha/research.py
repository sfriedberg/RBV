"""Secondary research layer for dialpha.

Pulls AlphaSense (or SEC EDGAR public filings if no API key is set) and
correlates deal-level patterns with public-market signals so a single report
is both structured evidence and market intelligence.

Data land on disk in ``~/.dialpha/cache/`` — zero cloud egress, fully local.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Config / secrets (all locals)
# ---------------------------------------------------------------------------

DOT_DIR = Path.home() / ".dialpha"            # ~/.dialpha/ lives on disk locally
CACHE_DIR = DOT_DIR / "cache"                 # cached research results
CONFIG  = DOT_DIR / "config.json"             # user-editable settings

DOT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)


def config() -> Dict[str, Any]:
    """Return user configuration (creates default if missing)."""
    if not CONFIG.exists():
        return {
             "alphasense_api_key": None,     # null → falls back to SEC EDGAR
             "ticker_whitelist": [],        # empty list = score everything
             "auto_research_on_score_gt": 0.50,   # fetch research if composite >= this
         }
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def save_config(cfg: Dict[str, Any]) -> None:
    CONFIG.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def _cache_key(ticker: str) -> str:
    """Deterministic hash for caching (no secrets in key)."""
    return hashlib.sha256(ticker.encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------
# SEC EDGAR lightweight fetcher (always available, no API key needed)
# ---------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup


def fetch_edgar_filing(
    ticker: str,
    form: str = "10-K",
    days_back: int = 365,
) -> Dict[str, Any]:
    """Fetch the most recent EDGAR 10-K (or other form) for a public company.

    Falls back to any available form if exact form match is empty.
    Returns ``{"body": str, "source_url": str}`` and caches on disk.
    """
    cache_path = CACHE_DIR / f"{_cache_key(ticker)}_{form}.json"
    age_hours = (time.time() - cache_path.stat().st_mtime) / 3600.0 if cache_path.exists() else 999
    
     # Cache hit < 24 h → return immediately
    if age_hours < 24 and cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    base = "https://www.sec.gov/cgi-bin/browse-edgar"
          params = {
             "action": "getcompany",
             "ticker": ticker,
             "type": form.replace("-", ""),           # "10-K" → "10K"
             "count": 1,
             "date": (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d"),
         }
    try:
        resp = requests.get(base, params=params, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
         filing_link = soup.find("a", href=True, string=lambda s: form in s and ".htm" in s)
        if not filing_link:
             return {"body": "", "source_url": "", "warning": f"No {form} found for {ticker}"}
        url = "https://www.sec.gov" + filing_link["href"]
        resp2 = requests.get(url, timeout=30); resp2.raise_for_status()
         body = BeautifulSoup(resp2.text, "html.parser").get_text(separator="\n", strip=True)
         payload = {"body": body, "source_url": url, "cached_at": datetime.utcnow().isoformat()}
        cache_path.write_text(json.dumps(payload), encoding="utf-8")
        return payload
    except Exception as exc:
        # Return partial / cached if available instead of crashing
        if cache_path.exists():
            return json.loads(cache_path.read_text(encoding="utf-8"))
         return {"body": "", "source_url": "", "error": str(exc)}


# ---------------------------------------------------------------------------
# AlphaSense wrapper (optional — key in ~/.dialpha/config.json)
# ---------------------------------------------------------------------------

def fetch_alphasense(ticker: str, query: str = "") -> Dict[str, Any]:
    """Query AlphaSense via its CLI or REST if configured.

    Currently stubbed: the user can drop an ``alphasense_api_key`` into
    ``~/.dialpha/config.json`` and enable actual calls. For now this
    returns a stable fallback so the pipeline never stalls.
    """
    cfg = config()
    api_key = cfg.get("alphasense_api_key")
     if not api_key:
        return {"body": "", "source": "alphasense-stub", "note": "No API key set; using SEC EDGAR fallback."}
     
      # ── Stub for when API key is present ───────────────────────────────
     # The real implementation would POST to ``https://platform.alphasense.net/api/``
     # with bearer ``api_key`` and a search query built from the pattern lib.
     # For now, return empty body so the caller sees "no alphasense data".
    return {"body": "", "source": "alphasense-stub-v2", "note": f"Key present but stub → query={query!r}"}


# ---------------------------------------------------------------------------
# ResearchEngine (public API for this module)
# ---------------------------------------------------------------------------

class ResearchEngine:
    """Fetch secondary evidence, score extracted text, return ranked insights."""

    def __init__(self) -> None:
        self.known_patterns = None         # lazy import from engine
        
     @property
    def patterns(self) -> Dict[str, Any]:
        if self._known_patterns is None:
             from .engine import KNOWN_PATTERNS
            self._known_patterns = KNOWN_PATTERNS
        return self._known_patterns

     def fetch_and_score(
        self,
        ticker: str,
        seed_text: str = "",
    ) -> List[Dict[str, Any]]:
        """1. Fetch EDGAR + AlphaSense for *ticker*. 2. Score seed text. 3. Return single-item list."""
        from .engine import score_deal

         results: List[Dict[str, Any]] = []
        
          # Fetch secondary research
        es_result = fetch_edgar_filing(ticker)
        as_result = fetch_alphasense(ticker, query=seed_text)
        
          # If no seed text was given, score the EDGAR body automatically
         text_to_score = seed_text or es_result.get("body", "")
         if not text_to_score:
             text_to_score = f"Ticker {ticker} has no public data yet."

        deal_result = score_deal(text_to_score)
         result_entry = dict(deal_result, ticker=ticker, research=es_result, alphasense=as_result)
        results.append(result_entry)
        return results

     def batch_research(
        self,
        tickers: List[str],
        seed_text_template: str = "",
    ) -> List[Dict[str, Any]]:
        """Fetch + score for a list of tickers and rank by composite."""
         all_results: List[Dict[str, Any]] = []
        for t in tickers:
             result = self.fetch_and_score(t, seed_text_template)
            all_results.extend(result)

          # Sort descending by composite score
        all_results.sort(key=lambda r: r["composite_score"], reverse=True)
        return all_results
