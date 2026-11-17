"""Visualizações calculadas exclusivamente do snapshot T4F validado."""
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure

from src.config import RAIZ
from src.resultados import carregar_resultados

AZUL, VERDE, LARANJA = "#175D78", "#258477", "#C87938"


def salvar(figura: Figure, nome: str, nota: str, esquerda: float = .09) -> None:
    figura.text(.08, .035, f"T4F | Dados sintéticos, seed 42 | {nota}", fontsize=9, color="#536579")
    figura.subplots_adjust(left=esquerda, right=.96, top=.84, bottom=.23)
    figura.savefig(RAIZ / "visualizacoes" / nome, dpi=150, facecolor="white")
    plt.close(figura)


def demanda(dados: dict[str, Any]) -> None:
    mensal = pd.DataFrame(dados["forecast"]["history"])
    sazonal = pd.DataFrame(dados["seasonality"]["months"])
    figura, eixos = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1.5, 1]})
    eixos[0].plot(range(len(mensal)), mensal.travelers, color=AZUL, marker="o", markersize=3)
    marcas = range(0, len(mensal), 6)
    eixos[0].set_xticks(list(marcas), mensal.month.iloc[list(marcas)], rotation=35, ha="right")
    eixos[0].set(title="Demanda histórica: 188 participações", ylabel="Viajantes confirmados / mês")
    eixos[1].bar(sazonal.month, sazonal["mean"], color=VERDE)
    eixos[1].set_xticks(range(1, 13))
    eixos[1].set(title="Média por mês do calendário", xlabel="Mês (2 ou 3 repetições)", ylabel="Viajantes / mês")
    salvar(figura, "demanda_sazonalidade.png", "Jan/2024 a out/2026; zeros conhecidos; sem prova inferencial de sazonalidade")


def cancelamentos(dados: dict[str, Any]) -> None:
    tabela = pd.DataFrame(dados["cancellations"]["groups"])
    tabela = tabela.loc[tabela.dimension.eq("Roteiro")].sort_values("rate")
    figura, eixo = plt.subplots(figsize=(11, 5))
    erros = np.array([tabela.rate - tabela.lower, tabela.upper - tabela.rate])
    eixo.errorbar(tabela.rate, range(len(tabela)), xerr=erros, fmt="o", color=AZUL, capsize=4)
    eixo.set_yticks(range(len(tabela)), [f"{r['name']} ({r['cancelled']}/{r['n']})" for r in tabela.to_dict("records")])
    eixo.set(title="Cancelamentos por roteiro: taxa e Wilson 95%", xlabel="Canceladas / todas as reservas do roteiro (%)", xlim=(0, 65))
    salvar(figura, "cancelamentos.png", "Histórico; n indicado; clientes podem repetir; intervalos não provam diferença", .28)


def satisfacao(dados: dict[str, Any]) -> None:
    grupos = [g for g in dados["satisfaction"]["groups"] if g["dimension"] == "Roteiro"]
    tabela = pd.DataFrame(grupos).sort_values("nps")
    figura, eixo = plt.subplots(figsize=(11, 5))
    eixo.barh(range(len(tabela)), tabela.nps, color=VERDE)
    eixo.set_yticks(range(len(tabela)), [f"{r['name']} (n={r['n']})" for r in tabela.to_dict("records")])
    eixo.set(title="NPS por roteiro: promotores menos detratores", xlabel="NPS (pontos; escala de -100 a 100)", xlim=(-100, 100))
    eixo.axvline(0, color="#718096", linewidth=1)
    salvar(figura, "satisfacao_nps.png", "72 respostas históricas; grupos pequenos e seleção de respondentes limitam comparações", .28)


def ocupacao(dados: dict[str, Any]) -> None:
    tabela = pd.DataFrame(dados["planning"]["slots"])
    grupos = tabela.groupby("routeName", sort=True)[["capacity", "committed", "shortage"]].sum()
    figura, eixo = plt.subplots(figsize=(12, 5))
    posicoes = np.arange(len(grupos))
    eixo.bar(posicoes - .18, grupos.capacity, width=.36, color=AZUL, label="Capacidade")
    eixo.bar(posicoes + .18, grupos.committed, width=.36, color=LARANJA, label="Comprometimento")
    eixo.set_xticks(posicoes, grupos.index)
    eixo.set(title="Planejamento: folga agregada não elimina déficits por slot", ylabel="Vagas-noite")
    eixo.set_ylim(0, grupos.capacity.max() * 1.35)
    eixo.legend(frameon=False, loc="upper right", ncols=2)
    for indice, falta in enumerate(grupos.shortage):
        eixo.text(indice, grupos.capacity.iloc[indice] + 2, f"Déficit: {falta}", ha="center", fontsize=10)
    salvar(figura, "ocupacao_planejamento.png", "07/11 a 31/12/2026; falta calculada antes de somar saída/data/etapa/categoria")


def financeiro(dados: dict[str, Any]) -> None:
    tabela = pd.DataFrame(dados["historical"]["routes"])
    figura, eixo = plt.subplots(figsize=(12, 5))
    posicoes = np.arange(len(tabela))
    for deslocamento, coluna, rotulo, cor in [(-.25, "revenue", "Receita contratada", AZUL),
                                             (0, "cost", "Custos", LARANJA),
                                             (.25, "contribution", "Contribuição", VERDE)]:
        eixo.bar(posicoes + deslocamento, tabela[coluna] / 1000, width=.25, label=rotulo, color=cor)
    eixo.set_xticks(posicoes, tabela.shortName, rotation=15, ha="right")
    eixo.set(title="Receita, custos e contribuição por roteiro", ylabel="Mil R$ demonstrativos")
    eixo.legend(frameon=False)
    salvar(figura, "financeiro_roteiros.png", "Jan/2024 a out/2026; contribuição = receita - custos; não é lucro líquido")


def previsao(dados: dict[str, Any]) -> None:
    modelo = dados["forecast"]
    historico, futuro = pd.DataFrame(modelo["history"]), pd.DataFrame(modelo["predictions"])
    figura, eixo = plt.subplots(figsize=(12, 5))
    eixo.plot(pd.to_datetime(historico.month), historico.travelers, color=AZUL, label="Histórico confirmado")
    eixo.plot(pd.to_datetime(futuro.month), futuro.predicted, "o--", color=LARANJA, label=modelo["selected"])
    if {"lower", "upper"}.issubset(futuro.columns):
        eixo.fill_between(pd.to_datetime(futuro.month), futuro.lower, futuro.upper, color=LARANJA, alpha=.15, label="Faixa exploratória")
    eixo.axvline(pd.Timestamp("2026-10-31"), color="#718096", linestyle=":")
    eixo.set(title="Previsão: seleção temporal antes do holdout", ylabel="Viajantes / mês", ylim=(0, None))
    eixo.legend(frameon=False, ncols=3)
    salvar(figura, "previsao_demanda.png", "Treino final até out/2026; faixas exploratórias sem cobertura nominal garantida")


def executar() -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold",
                         "axes.titlepad": 18, "axes.grid": True, "grid.alpha": .14,
                         "axes.axisbelow": True, "font.size": 10})
    dados = carregar_resultados()
    for gerar in (demanda, cancelamentos, satisfacao, ocupacao, financeiro, previsao):
        gerar(dados)


if __name__ == "__main__":
    executar()
