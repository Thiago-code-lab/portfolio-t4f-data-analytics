"""Orquestra o núcleo original e publica tabelas com reconciliação."""
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import BRUTOS, PROCESSADOS, RAIZ
from src.ingestao import verificar_fontes


def calcular(caminho: Path = BRUTOS) -> dict[str, Any]:
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("Node.js 22.12+ é necessário; consulte o README.")
    comando = [node, str(RAIZ / "node_modules/tsx/dist/cli.mjs"),
               str(RAIZ / "scripts/exportar-t4f.ts"), str(caminho)]
    resultado = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True,
                               encoding="utf-8", timeout=90, check=False)
    if resultado.returncode:
        raise ValueError(f"Núcleo T4F rejeitou a execução: {resultado.stderr.strip()}")
    return json.loads(resultado.stdout)


def validar_resultado(dados: dict[str, Any]) -> None:
    historico = dados["historical"]
    if sum(linha["travelers"] for linha in historico["monthly"]) != historico["travelers"]:
        raise ValueError("Participações mensais não reconciliam com o histórico.")
    if historico["totalRevenue"] != historico["realizedRevenue"] + historico["contractedFuture"]:
        raise ValueError("Receita contratada não reconcilia.")
    if sum(linha["revenue"] for linha in historico["routes"]) != historico["totalRevenue"]:
        raise ValueError("Receitas por roteiro não reconciliam.")
    if len(dados["forecast"]["history"]) != len(historico["monthly"]):
        raise ValueError("Calendários analítico e preditivo incompatíveis.")


def salvar_json(caminho: Path, dados: dict[str, Any]) -> None:
    temporario = caminho.with_suffix(caminho.suffix + ".part")
    temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporario.replace(caminho)


def executar() -> None:
    manifesto = verificar_fontes()
    dados = calcular()
    validar_resultado(dados)
    if dados["datasetSha256"] != manifesto["dataset"]["sha256"]:
        raise ValueError("Snapshot mudou durante a execução.")
    PROCESSADOS.mkdir(parents=True, exist_ok=True)
    tabelas = {"demanda_mensal": dados["historical"]["monthly"],
               "roteiros": dados["historical"]["routes"], "sazonalidade": dados["seasonality"]["months"],
               "cancelamentos": dados["cancellations"]["groups"],
               "satisfacao": dados["satisfaction"]["groups"],
               "previsoes": dados["forecast"]["predictions"],
               "ocupacao_planejamento": dados["planning"]["slots"]}
    for nome, registros in tabelas.items():
        destino = PROCESSADOS / f"{nome}.csv"
        temporario = destino.with_suffix(".csv.part")
        pd.DataFrame(registros).to_csv(temporario, index=False, encoding="utf-8")
        temporario.replace(destino)
    salvar_json(PROCESSADOS / "analise-t4f.json", dados)
    print(f"T4F validado: {dados['counts']['bookings']} reservas na base; {dados['historical']['travelers']} participações históricas.")


if __name__ == "__main__":
    executar()
