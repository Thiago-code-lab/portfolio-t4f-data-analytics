"""Confere o gerador original em diretório temporário, sem tocar na fonte."""
import runpy
import tempfile
from pathlib import Path

from src.config import BRUTOS, RAIZ
from src.ingestao import sha256


def verificar_gerador() -> str:
    namespace = runpy.run_path(str(RAIZ / "vendor/t4f/scripts/generate_demo_data.py"))
    with tempfile.TemporaryDirectory(prefix="t4f-demo-") as pasta:
        namespace["main"].__globals__["ROOT"] = Path(pasta)
        namespace["main"]()
        gerado = Path(pasta) / "public/data/demo.json"
        if gerado.read_bytes() != BRUTOS.read_bytes():
            raise ValueError("Gerador não reproduziu o snapshot byte a byte.")
    return sha256(BRUTOS)


if __name__ == "__main__":
    print(f"Gerador seed 42 reproduzido: {verificar_gerador()}")
