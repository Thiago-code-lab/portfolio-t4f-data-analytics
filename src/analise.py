"""Diagnóstico estrutural; não representa análise de negócio."""

from collections.abc import Iterable
from typing import TypedDict


class Diagnostico(TypedDict):
    colunas: list[str]
    linhas: int
    ausencias: dict[str, int]


def diagnosticar(registros: Iterable[tuple[str, ...]]) -> Diagnostico:
    """Conta ausências sem materializar toda a base em memória."""
    fluxo = iter(registros)
    cabecalho = next(fluxo, ())
    if not cabecalho or len(set(cabecalho)) != len(cabecalho):
        raise ValueError("Cabeçalho ausente ou duplicado.")
    ausencias = dict.fromkeys(cabecalho, 0)
    linhas = 0
    for registro in fluxo:
        if len(registro) != len(cabecalho):
            raise ValueError("Registro não corresponde ao cabeçalho.")
        linhas += 1
        for nome, valor in zip(cabecalho, registro, strict=True):
            if not valor.strip():
                ausencias[nome] += 1
    if not linhas:
        raise ValueError("A base não contém registros de dados.")
    return {"colunas": list(cabecalho), "linhas": linhas, "ausencias": ausencias}
