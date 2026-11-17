"""Verificação offline das fontes públicas incorporadas, sem downloads em reruns."""
import hashlib
import json
from pathlib import Path

from src.config import RAIZ


def sha256(caminho: Path) -> str:
    with caminho.open("rb") as arquivo:
        return hashlib.file_digest(arquivo, "sha256").hexdigest()


def verificar_fontes() -> dict[str, object]:
    manifesto = json.loads((RAIZ / "docs/fontes.json").read_text(encoding="utf-8"))
    for registro in [manifesto["dataset"], *manifesto["files"]]:
        caminho = (RAIZ / registro["local"]).resolve()
        caminho.relative_to(RAIZ)
        if sha256(caminho) != registro["sha256"]:
            raise ValueError(f"Fonte alterada: {registro['local']}")
    return manifesto


if __name__ == "__main__":
    print(json.dumps(verificar_fontes(), ensure_ascii=False, indent=2))
