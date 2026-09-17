"""Flask routes for the dialpha local dashboard.

``create_app()`` is the single factory used by ``dialpha serve`` and tests.
"""

from __future__ import annotations

from typing import Any

from flask import Flask, jsonify, render_template_string, request

from ..engine import KNOWN_PATTERNS, score_batch, score_deal
from ..research import ResearchEngine
from .templates import INDEX_HTML

__all__ = ["create_app"]


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        return render_template_string(INDEX_HTML)

    @app.route("/api/score", methods=["POST"])
    def api_score() -> Any:
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()
        if not text:
            return jsonify({"error": "No text provided"}), 400
        return jsonify(score_deal(text))

    @app.route("/api/batch", methods=["POST"])
    def api_batch() -> Any:
        data = request.get_json(silent=True) or {}
        files = data.get("files") or []
        if not files:
            return jsonify({"error": "No files provided"}), 400
        return jsonify(score_batch(files))

    @app.route("/api/patterns", methods=["GET"])
    def api_patterns() -> Any:
        return jsonify({
            name: {
                "name": p.name,
                "weight": p.weight,
                "threshold": p.threshold,
                "direction": p.direction,
            }
            for name, p in KNOWN_PATTERNS.items()
        })

    @app.route("/api/research", methods=["POST"])
    def api_research() -> Any:
        data = request.get_json(silent=True) or {}
        ticker = (data.get("ticker") or "").strip().upper()
        if not ticker:
            return jsonify({"error": "No ticker provided"}), 400
        engine = ResearchEngine()
        return jsonify(engine.fetch_and_score(ticker))

    return app
