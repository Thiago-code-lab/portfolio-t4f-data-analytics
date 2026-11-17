"""Interface de linha de comando para diagnóstico local de CSV."""

import argparse
import csv
import json
import sys
from contextlib import closing
from pathlib import Path

from src.analise import diagnosticar
from src.carregar_dados import ler_csv


def main(argumentos: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Diagnosticar estrutura e ausências em CSV.")
    parser.add_argument("caminho", type=Path, help="Arquivo CSV local com cabeçalho.")
    parser.add_argument("--delimiter", default=";", help="Separador de campos (padrão: ;).")
    parser.add_argument("--encoding", default="utf-8-sig", help="Encoding (padrão: utf-8-sig).")
    opcoes = parser.parse_args(argumentos)
    try:
        with closing(ler_csv(opcoes.caminho, opcoes.delimiter, opcoes.encoding)) as registros:
            resultado = diagnosticar(registros)
    except (OSError, UnicodeError, csv.Error, ValueError, LookupError) as erro:
        print(f"Falha no diagnóstico: {erro}", file=sys.stderr)
        return 2
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
