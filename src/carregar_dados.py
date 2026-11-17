"""Leitura incremental com validação estrutural explícita."""

import csv
from collections.abc import Iterator
from pathlib import Path


def ler_csv(
    caminho: Path, delimitador: str = ";", encoding: str = "utf-8-sig"
) -> Iterator[tuple[str, ...]]:
    """Produz cabeçalho e registros; rejeita estruturas ambíguas."""
    if len(delimitador) != 1 or delimitador in "\r\n\x00\"":
        raise ValueError("Delimitador deve ser um caractere distinto de aspas e quebras.")
    with caminho.open("r", encoding=encoding, newline="") as arquivo:
        leitor = csv.reader(arquivo, delimiter=delimitador, strict=True)
        cabecalho = tuple(next(leitor, ()))
        if not cabecalho or any(not nome or nome != nome.strip() for nome in cabecalho):
            raise ValueError("Cabeçalho ausente, vazio ou com espaços nas extremidades.")
        if len(set(cabecalho)) != len(cabecalho):
            raise ValueError("Cabeçalho contém colunas duplicadas.")
        yield cabecalho
        for registro in leitor:
            if len(registro) != len(cabecalho):
                raise ValueError(f"Largura inconsistente na linha física {leitor.line_num}.")
            yield tuple(registro)
