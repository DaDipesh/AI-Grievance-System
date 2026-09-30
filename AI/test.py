import pandas as pd
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

AI_DIR = Path(__file__).resolve().parent
data = pd.read_csv(AI_DIR / "dataset" / "complaints.csv")
print(data)
print(data.shape)
print(data.columns)
