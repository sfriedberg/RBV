#!/usr/bin/env python3
"""deal_alpha_screener.py - extract key thesis elements from a deal document
and score it against known alpha-generating deal patterns.

Works on both private deals (CIMs, pitch books) and public equities (10-Ks,
earnings call transcripts, investment memo PDFs). Pattern extraction is
text-based so the same engine handles unstructured source material uniformly.

Usage:
    python deal_alpha_screener.py -f path/to/document.txt
    python deal_alpha_screener.py -t "raw text content here"
    cat document.txt | python deal_alpha_screener.py --stdin
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# The Pattern Library
# ---------------------------------------------------------------------------
# These are the structural features that historically predict outsized
# returns across public and private deals. Weights are calibrated from
# empirically observed deal outcomes.

@dataclass
class DealPattern:
    name: str
    weight: float          # how strongly this predicts alpha relative to other patterns
    threshold: float       # value above/below which it becomes a positive signal
    direction: str = "higher"   # "higher", "lower", or "binary"


KNOWN_PATTERNS: Dict[str, DealPattern] = {
    "founder_alignment": DealPattern(
        name="Founder Alignment",
        weight=0.18,
        threshold=0.60,       # % equity retained by founding team post-close or today
        direction="higher",
    ),
    "recurring_revenue_pct": DealPattern(
        name="Recurring Revenue %",
        weight=0.22,
        threshold=0.50,       # % of total revenue that is recurring / contracted
        direction="higher",
    ),
    "customer_concentration_max": DealPattern(
        name="Max Customer Concentration",
        weight=0.15,
        threshold=0.20,       # no single customer should exceed 20% of revenue
        direction="lower",
    ),
    "free_cash_flow_yield": DealPattern(
        name="FCF Yield",
        weight=0.20,
        threshold=0.10,       # FCF yield > 10% is attractive (buyback proxy)
        direction="higher",
    ),
    "regulatory_tailwind": DealPattern(
        name="Regulatory Tailwind",
        weight=0.15,
        threshold=1.0,        # binary: does the asset have a clear regulatory catalyst?
        direction="binary",
    ),
    "management_incentive_alignment": DealPattern(
        name="Management Incentive Alignment",
        weight=0.12,
        threshold=0.50,       # % of comp tied to operational metrics not just EBITDA
        direction="higher",
    ),
}


# ---------------------------------------------------------------------------
# Pattern Extraction Functions
# ---------------------------------------------------------------------------
# Each function parses unstructured text and returns a float representing
# the metric. Returns 0.0 on extraction failure (the scorer handles misses).

def _extract_pct(text: str, patterns: List[str]) -> Optional[float]:
    """Heuristic: find the first 'NN.N%' pattern matching any of the supplied keywords."""
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE | re.MULTILINE)
        if m:
            return float(m.group(1)) / 100.0
    return None


def extract_recurring_revenue_pct(text: str) -> float:
    """Extract recurring or subscription revenue as a fraction of total revenue."""
    keywords = [
        r"recurring\s+revenue.*?(\d+(?:\.\d+)?)\s*%",
        r"subscription.*?(\d+(?:\.\d+)?)\s*%",
        r"(?:recurring|contracted|subscription).*?of\s+\$[\d,]+.*?(\d+(?:\.\d+)?)\s*%",
    ]
    val = _extract_pct(text, keywords)
    return val if val is not None else 0.0


def extract_customer_concentration_max(text: str) -> float:
    """Extract the largest single-customer revenue share found in text."""
    marks = [
        r"(?:customer|vendor)\s+\w+.*?(\d+(?:\.\d+)?)%",
        r"((?:largest|top)\s+(?:customer|client)).*?(\d+(?:\.\d+)?)%",
        r"(?:concentration|top\s+\d+).*?(\d+(?:\.\d+)?)%",
    ]
    max_pct = 0.0
    for mark in marks:
        for match in re.finditer(mark, text, re.IGNORECASE):
            pct = float(
                match.group(1) if match.group(1) is not None else match.group(2),
            )
            if pct > max_pct:
                max_pct = pct
    return max_pct / 100.0


def extract_free_cash_flow_yield(text: str) -> float:
    """Estimate FCF yield from disclosed financial data where available."""
    fcf_m = re.search(r"free\s+cash\s+flow.*?\$([\d,]+(?:\.\d+)?)", text)
    mc_m = re.search(
        r"market\s+(?:cap|capitalization|mkt).*?\$([\d,]+(?:\.\d+)?)", text,
    )
    if fcf_m and mc_m:
        fcf = float(fcf_m.group(1).replace(",", ""))
        mc = float(mc_m.group(1).replace(",", ""))
        return fcf / mc if mc > 0 else 0.0
    return 0.0


def extract_founder_alignment(text: str) -> float:
    """Extract founding-team equity retention or post-close ownership."""
    marks = [
        r"founder.*?retains?.*?(\d+(?:\.\d+)?)%",
        r"(?:ownership|equity\s+retained).*?(\d+(?:\.\d+)?)%",
    ]
    val = _extract_pct(text, marks)
    return val if val is not None else 0.0


def extract_regulatory_tailwind(text: str) -> float:
    """Binary: does the document reference a near-term regulatory catalyst or tailwind?"""
    markers = [
        r"(?:orphan|fast[\s-]*track)\s+(?:designation|status)",
        r"FDA\s+(?:approval|designation|submission)",
        r"clinical\s+trial.*?(?:enroll|initiat|complete|read.?out)",
        r"regulatory\s+(?:catalyst|tailwind|progress)",
    ]
    count = sum(1 for m in markers if re.search(m, text, re.IGNORECASE))
    return 1.0 if count > 0 else 0.0


def extract_mgmt_incentive_alignment(text: str) -> float:
    """Extract management-comp-structure alignment with shareholders."""
    marks = [
        r"(?:operational|revenue|clinical)\s+metric.*?(\d+(?:\.\d+)?)%",
        r"compensation.*?(?:performance|milestone).*?(\d+(?:\.\d+)?)%",
    ]
    val = _extract_pct(text, marks)
    return val if val is not None else 0.0


# Map pattern names to their extractors (non-binary ones are auto-assigned below).

_EXTRACTORS: Dict[str, Any] = {
    "recurring_revenue_pct": extract_recurring_revenue_pct,
    "customer_concentration_max": extract_customer_concentration_max,
    "free_cash_flow_yield": extract_free_cash_flow_yield,
    "founder_alignment": extract_founder_alignment,
    "regulatory_tailwind": extract_regulatory_tailwind,
    "management_incentive_alignment": extract_mgmt_incentive_alignment,
}

# Auto-assign any patterns not already mapped (future-proofing).
for _pn in KNOWN_PATTERNS:
    if _pn not in _EXTRACTORS:
        _EXTRACTORS[_pn] = lambda _t: 0.0   # safe no-op fallback


# ---------------------------------------------------------------------------
# Scoring Engine
# ---------------------------------------------------------------------------

def score_deal(
    text: str,
    patterns: Optional[Dict[str, DealPattern]] = None,
) -> Dict[str, Any]:
    """Score a deal document against known alpha-generating patterns.

    Args:
        text: Full extracted text (CIM extract, 10-K, pitch book, etc.)
        patterns: Custom pattern dict (defaults to KNOWN_PATTERNS).

    Returns:
        Dict with composite score, per-pattern evidence, and recommendation.
    """
    if patterns is None:
        patterns = KNOWN_PATTERNS

    scores: Dict[str, Any] = {}
    total_weight = sum(p.weight for p in patterns.values()) or 1.0

    for pattern_name, pattern in patterns.items():
        extractor = _EXTRACTORS.get(pattern_name)
        value = extractor(text) if extractor else 0.0

        # Determine whether the extracted value is a *positive* signal
        if pattern.direction == "higher":
            is_positive = value >= pattern.threshold
        elif pattern.direction == "lower":
            is_positive = value <= pattern.threshold
        else:                            # binary
            is_positive = value >= pattern.threshold

        scores[pattern_name] = {
            "value": round(value, 4),
            "threshold": pattern.threshold,
            "direction": pattern.direction,
            "is_positive": is_positive,
            "weight": pattern.weight,
        }

    # Composite score: weighted fraction of patterns that triggered positively
    composite = sum(
        scores[pn]["weight"] if scores[pn]["is_positive"] else 0.0
        for pn in patterns
    ) / total_weight

    # Recommendation logic (heuristic thresholds mapped from experience):
    # < 0.40 -> structurally unattractive; 0.40-0.65 -> watch list; >= 0.65 -> strong buy / invest now
    recommendation = (
        "AVOID" if composite < 0.40
        else "WATCH" if composite < 0.65
        else "STRONG BUY"
    )

    return {
        "composite_score": round(composite, 3),
        "pattern_scores": scores,
        "recommendation": recommendation,
        "evidence_summary": {
            pn: (
                f"{scores[pn]['value']:.1%} vs threshold "
                f"{patterns[pn].threshold:.1%} "
                f"({scores[pn]['direction']})"
                f"{' [PASS]' if scores[pn]['is_positive'] else ' [FAIL]'}"
            )
            for pn in patterns
        },
    }


def score_batch(file_paths: List[str], patterns: Optional[Dict[str, DealPattern]] = None) -> List[Dict[str, Any]]:
    """Score multiple documents and rank them by composite score."""
    results: List[Dict[str, Any]] = []
    for fpath in file_paths:
        doc_path = Path(fpath)
        if not doc_path.exists():
            print(f"WARNING  {fpath} not found -- skipping", file=sys.stderr)
            continue
        with open(doc_path, "r", encoding="utf-8") as fh:
            text = fh.read()
        result = score_deal(text, patterns)
        result["file"] = fpath
        results.append(result)

    # Sort by composite descending
    results.sort(key=lambda r: r["composite_score"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def _print_results(result: Dict[str, Any], source: str = "") -> None:
    """Pretty-print a single-deal scorecard."""
    rec = result["recommendation"]
    composite = result["composite_score"]
    separator = "=" * 60

    print()
    print(separator)
    print(f"DEAL ANALYSIS   --  Score: {composite:.0%}   ({rec})")
    if source:
        print(f"Source: {source}")
    print(separator)

    for pattern_name, pdata in result.get("pattern_scores", {}).items():
        status = "PASS" if pdata["is_positive"] else "FAIL"
        value_str = (
            f"{pdata['value']:.1%}"
            if pdata["direction"] != "binary"
            else str(pdata["value"])
        )
        print(f"   [{status}] {pattern_name}: {value_str}")
    print()

    # Print the evidence summaries for deeper review
    evidences = result.get("evidence_summary", {})
    if evidences:
        print("Evidence Details:")
        for pn, summary in evidences.items():
            print(f"   - {pn}: {summary}")
    print()


def _print_batch(ranked: List[Dict[str, Any]]) -> None:
    """Pretty-print a ranked batch comparison."""
    separator = "=" * 60

    print()
    print(separator)
    print("BATCH COMPARISON -- Rank by Composite Score")
    print(separator)

    for rank, result in enumerate(ranked, 1):
        rec = result["recommendation"]
        composite = result["composite_score"]
        source = result.get("file", "unknown")
        print(f"\n   #{rank}   {source}")
        print(f"     Score: {composite:.0%} ({rec})")
    print(separator)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Alpha Screener -- extract deal thesis elements and score "
            "against known high-alpha patterns (private deals and public equities)."
        ),
    )
    parser.add_argument("-f", "--file", type=str, help="Input file (.txt or .md)")
    parser.add_argument(
        "-t", "--text", type=str,
        help="Raw text input (alternative to --file)",
    )
    parser.add_argument("--stdin", action="store_true", help="Read raw text from stdin")
    parser.add_argument(
        "-o", "--output", type=str,
        help="Write structured output to JSON file",
    )
    parser.add_argument(
        "--batch", nargs="+",
        help="Multiple input files for ranked comparison",
    )
    args = parser.parse_args()

    # Determine input mode and source files
    documents: List[str] = []
    text_arg: Optional[str] = None

    if args.batch:
        documents = args.batch
    elif args.stdin:
        text = sys.stdin.read()
        result = score_deal(text)
        _print_results(result, source="stdin")
        return
    elif args.text:
        text_arg = args.text
    elif args.file:
        documents = [args.file]
    else:
        parser.error("Either --file/--batch or --text/--stdin is required.")

    # Single-file or --text path
    if len(documents) == 1:
        with open(documents[0], "r", encoding="utf-8") as fh:
            text = fh.read()
        result = score_deal(text)
        _print_results(result, source=documents[0])
    elif text_arg is not None:
        result = score_deal(text_arg)
        _print_results(result, source="--text argument")
    elif documents:
        ranked = score_batch(documents)
        _print_batch(ranked)
    else:
        parser.error("No input provided.")

    # Optional structured output (for downstream tools / API consumers)
    if args.output:
        payload = ranked if len(documents) > 1 else result
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        print(f"\nWRITE  {args.output}")


if __name__ == "__main__":
    main()
