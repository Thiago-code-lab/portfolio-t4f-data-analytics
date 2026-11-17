"""Caminhos e referência imutável da análise demonstrativa T4F."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "data/raw/t4f-demo.json"
PROCESSADOS = RAIZ / "data/processed"
COMMIT_ORIGINAL = "0216dce5f67b83fbb0ba84346a7742dcb4f5ce23"
