from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AI_DIR = PROJECT_ROOT.parent / "AI"

if str(AI_DIR) not in sys.path:
    sys.path.insert(0, str(AI_DIR))


# ---------------------------------------------------------
# AI Engine
# ---------------------------------------------------------

from prediction.ai_engine import analyze_with_ai


# ---------------------------------------------------------
# Backend AI Service
# ---------------------------------------------------------

def analyze_complaint_with_ai(
    complaint_text: str,
    *,
    city: str | None = None,
    district: str | None = None,
    area: str | None = None,
    image_path: str | None = None,
) -> dict[str, Any]:
    """
    Run the existing AI grievance engine.

    Production complaints are NOT automatically added
    to the training dataset.
    """

    return analyze_with_ai(
        complaint=complaint_text,
        city=city,
        district=district,
        area=area,
        image_path=image_path,
        save_to_dataset=False,
    )