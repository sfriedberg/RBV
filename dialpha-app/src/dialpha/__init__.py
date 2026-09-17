"""dialpha — Deal Alpha: extract deal patterns, score alpha signals."""

from .engine import KNOWN_PATTERNS, DealPattern, score_deal, score_batch

__version__ = "0.1.0"

__all__ = [
    "KNOWN_PATTERNS",
    "DealPattern",
    "score_deal",
    "score_batch",
    "__version__",
]
