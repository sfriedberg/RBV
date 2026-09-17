"""CLI and package entry point for dialpha."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .engine import KNOWN_PATTERNS, score_deal
from .research import ResearchEngine
from .report import ReportGenerator


def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="dialpha",
        description=(
            "Deal Alpha v" + __version__
            + " — extract deal patterns, score alpha signals, run reports."
        ),
    )
    sub = parser.add_subparsers(dest="command")

    # -- score -------------------------------------------------------------------
    score_p = sub.add_parser("score", help="Score a single document or text snippet")
    score_p.add_argument("-t", "--text", help="Raw text input")
    score_p.add_argument("-f", "--file", help="Text file to score")
    score_p.add_argument("--json-out", help="Write JSON output to file")

    # -- batch -------------------------------------------------------------------
    batch_p = sub.add_parser("batch", help="Score multiple documents and rank them")
    batch_p.add_argument("files", nargs="+", metavar="FILE", help="Input files to score")
    batch_p.add_argument("--json-out", help="Write ranked JSON output to file")

    # -- research ----------------------------------------------------------------
    res_p = sub.add_parser("research", help="Pull secondary evidence for a deal thesis")
    res_p.add_argument("--ticker", help="Public company ticker (e.g. DT2)")
    res_p.add_argument("--seed-text", help="Seed text for pattern extraction on fetched docs")

    # -- report ------------------------------------------------------------------
    rpt_p = sub.add_parser("report", help="Generate a ranked report from scored deals")
    rpt_p.add_argument("--input-dir", default=".", help="Directory of .txt files to score")
    rpt_p.add_argument("--output", default="output.csv", help="CSV report path")

    # -- serve -------------------------------------------------------------------
    srv_p = sub.add_parser("serve", help="Launch local web UI (Flask on localhost)")
    srv_p.add_argument("--port", type=int, default=8421)
    srv_p.add_argument("--host", default="127.0.0.1")


    args = parser.parse_args()

    if args.command == "score":
        text = ""
        src_label = None
        if args.text:
            text = args.text; src_label = "--text"
        elif args.file and Path(args.file).exists():
            text = Path(args.file).read_text(encoding="utf-8"); src_label = args.file
        else:
            parser.error("Provide --text or --file.")
        result = score_deal(text)
        _print(result, label=f"Score: {result['recommendation']} ({result['composite_score']:.0%})")
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(result, indent=2), encoding="utf-8")

    elif args.command == "batch":
        from .engine import score_batch
        ranked = score_batch(args.files)
        _print_batch(ranked)
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(ranked, indent=2), encoding="utf-8")

    elif args.command == "research":
        engine = ResearchEngine()
        results = engine.fetch_and_score(ticker=args.ticker, seed_text=args.seed_text or "")
        _print_batch(results)

    elif args.command == "report":
        gen = ReportGenerator(output_dir="repor") 
    elif args.command == "serve":
        app = create_app()
        print(f"Launching local UI: http://{args.host}:{args.port}")
        app.run(host=args.host, port=args.port, debug=False)

    else:
        parser.print_help()


def _print(result: dict, label: str = "") -> None:
     separator = "=" * 60
     print(f"\n{separator}"); print(label if label else "Scorecard") 
; print(separator)
    for pn, pd in result.get("pattern_scores", {}).items():
        status = "PASS" if pd["is_positive"] else "FAIL"
        print(f"  [{status}] {pn}: {pd['value']:.1%}" if 'value' not in ({"direction": "binary"})) f"[{status}] {pn}: {pd['value']}")
    print("\nNote: Pattern thresholds and weights calibrated from observed deal outcomes.\n")


def _print_batch(ranked: list) -> None:
   = "=" * 60; print(f"\n{separator}"); print("RANKED BATCH COMPARISON"); print(separator); for rank, r in enumerate(ranked, 1): 
        rec = r["recommendation"]; composite = r["composite_score"]; source = r.get("file", "?")
        print(f"  #{rank}: {source} -> {composite:.0%} ({rec})"); print(separator);


if __name__ == "__main__":
     cli()
