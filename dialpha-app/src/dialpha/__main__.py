"""CLI and package entry point for dialpha.

Run from the virtualenv:
    .venv/bin/python -m pip install -e .          # editable install
    .venv/bin/python -m dialpha --help             # CLI help
    .venv/bin/python -m dialpha score -t "..."     # score raw text
    .venv/bin/python -m dialpha batch *.txt         # batch-score files
    .venv/bin/python -m dialpha serve              # launch Flask UI at :8421

Or skip the editable install and do:
    PYTHONPATH=src python -m dialpha --help
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .engine import KNOWN_PATTERNS, score_deal, score_batch, _print_result, _print_batch

# ── CLI parser ────────────────────────────────────────────────────────────────


def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="dialpha",
        description=(
            "Deal Alpha v" + __version__
            + "  -- extract deal patterns and score alpha signals."
        ),
    )
    sub = parser.add_subparsers(dest="command")

    # -- score -------------------------------------------------------------------
    score_p = sub.add_parser(
        "score", help="Score a single document or text snippet"
    )
    score_p.add_argument("-t", "--text", help="Raw text input")
    score_p.add_argument("-f", "--file", help="Text file to score")
    score_p.add_argument("--json-out", help="Write JSON output to file")

    # -- batch -------------------------------------------------------------------
    batch_p = sub.add_parser(
        "batch", help="Score multiple documents and rank them"
    )
    batch_p.add_argument(
        "files", nargs="+", metavar="FILE", help="Input files to score"
    )
    batch_p.add_argument("--json-out", help="Write ranked JSON output to file")

    # -- serve -------------------------------------------------------------------
    srv_p = sub.add_parser("serve", help="Launch local web UI (Flask on localhost)")
    srv_p.add_argument("--port", type=int, default=8421)
    srv_p.add_argument("--host", default="127.0.0.1")

    # -- no command given → print help -------------------------------------------
    args = parser.parse_args()

    if args.command == "score":
        text, label = "", ""
        if args.text:
            text, label = args.text, "stdin"
        elif args.file and Path(args.file).exists():
            text = Path(args.file).read_text(encoding="utf-8")
            label = args.file
        else:
            parser.error("Provide --text or an existing --file.")
        result = score_deal(text)
        _print_result(result, source=label)
        if args.json_out:
            Path(args.json_out).write_text(
                json.dumps(result, indent=2), encoding="utf-8"
            )

    elif args.command == "batch":
        ranked = score_batch(args.files)
        _print_batch(ranked)
        if args.json_out:
            Path(args.json_out).write_text(
                json.dumps(ranked, indent=2), encoding="utf-8"
            )

    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
