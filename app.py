"""Leitor leve do portfólio; não executa modelos ou ingestão em interações."""
import json
from typing import Any

import pandas as pd
import streamlit as st

from src.config import PROCESSADOS, RAIZ
from src.resultados import formatar

st.set_page_config(page_title="T4F | Portfólio analítico", page_icon="📊", layout="wide")


@st.cache_data(show_spinner=False)
def carregar(versao: int, caminho: str) -> dict[str, Any]:
    """mtime invalida o cache; leitura limitada ao artefato local validado."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def indicadores(resumo: dict[str, Any]) -> None:
    colunas = st.columns(4)
    valores = [("Participações", str(resumo["travelers"])),
               ("NPS (pontos)", "—" if resumo["nps"] is None else formatar(resumo["nps"])),
               ("Ocupação em vagas-noite", "—" if resumo["occupancy"] is None else f"{formatar(resumo['occupancy'])}%"),
               ("Receita contratada (R$)", formatar(resumo["totalRevenue"]))]
    for coluna, (rotulo, valor) in zip(colunas, valores, strict=True):
        coluna.metric(rotulo, valor)


def historico(dados: dict[str, Any]) -> None:
    nomes = {linha["id"]: linha["routes"][0]["shortName"] for linha in dados["byRoute"]}
    escolhido = st.sidebar.selectbox("Roteiro histórico", ["all", *nomes], format_func=lambda chave: nomes.get(chave, "Todos"))
    resumo = dados["historical"] if escolhido == "all" else next(linha for linha in dados["byRoute"] if linha["id"] == escolhido)
    st.caption("Histórico: 01/01/2024 a 31/10/2026. Coorte de viagens; conversão usa coorte de primeiro contato.")
    indicadores(resumo)
    mensal = pd.DataFrame(resumo["monthly"]).set_index("month")
    st.subheader("Demanda mensal confirmada")
    st.line_chart(mensal[["travelers"]])
    st.subheader("Receita, custos e contribuição")
    financeiro = mensal[["revenue", "cost"]].copy()
    financeiro["contribution"] = financeiro.revenue - financeiro.cost
    st.bar_chart(financeiro)
    st.caption(f"{resumo['responses']} respostas; cancelamentos {formatar(resumo['cancellationRate'])}%. Receita não deve ser somada aos recebimentos; contribuição não é lucro líquido.")
    st.download_button("Baixar histórico do recorte", mensal.to_csv().encode("utf-8-sig"), "t4f-historico.csv", "text/csv")


def apresentar() -> None:
    st.title("T4F Performance | Portfólio de Data Analytics")
    st.info("Dados demonstrativos sintéticos. Os números não representam o desempenho real da Tour4Friends.")
    caminho = PROCESSADOS / "analise-t4f.json"
    try:
        dados = carregar(caminho.stat().st_mtime_ns, str(caminho))
    except (OSError, ValueError) as erro:
        st.error(f"Análise indisponível: {erro}")
        st.code("npm ci\npython -m src.executar")
        st.stop()
    viagens, planejamento, evidencias = st.tabs(["Histórico", "Planejamento global", "Método e evidências"])
    with viagens:
        historico(dados)
    with planejamento:
        st.caption("Recorte global independente do filtro histórico: 07/11 a 31/12/2026. Valores contratados/estimados no cenário.")
        plano = dados["planning"]
        st.warning(f"{plano['shortage']} vagas-noite em falta por slot, com ocupação agregada de {formatar(plano['occupancy'])}%.")
        st.image(str(RAIZ / "visualizacoes/ocupacao_planejamento.png"))
        st.dataframe(pd.DataFrame(plano["slots"])[["routeName", "date", "locality", "category", "capacity", "committed", "shortage"]], hide_index=True)
    with evidencias:
        st.write("O núcleo TypeScript original valida o snapshot e calcula indicadores e modelos. Python publica tabelas, gráficos, notebook e PDF. A interface lê o resultado com cache por versão do arquivo.")
        st.write("CRISP-DM e KDD relacionados a artefatos reais; Scrum e Kanban com limites explícitos. Série curta, amostra sintética e faixas exploratórias impedem inferir desempenho real.")
        st.link_button("Projeto Integrador V original", "https://github.com/Thiago-code-lab/Dashboards-Tour4Friends")
        st.code(dados["datasetSha256"], language=None)


if __name__ == "__main__":
    apresentar()
