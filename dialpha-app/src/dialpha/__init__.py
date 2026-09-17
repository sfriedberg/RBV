"""dialpha — Deal Alpha: extract deal patterns, score alpha signals, run reports."""

__version__ = "0.1.0"

from dialpha.engine import (
    KNOWN_PATTERNS,
    DealPattern,
    score_deal,
)
from dialpha.research import ResearchEngine
from dialpha.scheduler import WeeklyScheduler
from dialpha.web.api import create_app

__all__ = [
    "KNOWN_PATTERNS",
    "DealPattern",
    "score_deal",
    "ResearchEngine",
    "WeeklyScheduler",
    "create_app",
]
