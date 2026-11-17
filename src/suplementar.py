"""Validação separada do pacote acadêmico fornecido: outra moeda e taxonomia."""
import json
from typing import Any

import numpy as np
import pandas as pd

from src.config import PROCESSADOS, RAIZ
from src.executar import salvar_json
from src.ingestao import sha256

PASTA = RAIZ / "data/suplementar"
REFERENCIA = pd.Timestamp("2026-11-16")
CATEGORIAS = {"Econômico", "Standard", "Superior"}


def carregar() -> dict[str, pd.DataFrame]:
    manifesto = json.loads((RAIZ / "docs/anexos-manifesto.json").read_text(encoding="utf-8"))
    pacote = manifesto["zip"]
    if sha256(RAIZ / pacote["arquivo"]) != pacote["sha256"]:
        raise ValueError("ZIP complementar alterado.")
    tabelas = {}
    for registro in pacote["conteudo"]:
        if registro["arquivo"].endswith(".csv"):
            caminho = PASTA / registro["arquivo"]
            if sha256(caminho) != registro["sha256"]:
                raise ValueError(f"CSV alterado: {caminho.name}")
            tabelas[caminho.stem] = pd.read_csv(caminho, encoding="utf-8-sig")
    return tabelas


def exigir(condicao: bool, mensagem: str) -> None:
    if not condicao:
        raise ValueError(mensagem)


def validar(tabelas: dict[str, pd.DataFrame]) -> None:
    clientes, reservas = tabelas["sintetico_clientes"], tabelas["sintetico_reservas"]
    feedback = tabelas["sintetico_feedbacks_nps"]
    for tabela, chave in ((clientes, "id_cliente"), (reservas, "id_reserva"), (feedback, "id_feedback")):
        exigir(tabela[chave].notna().all() and tabela[chave].is_unique, f"Chave inválida: {chave}")
    exigir(reservas.id_cliente.isin(clientes.id_cliente).all(), "Cliente não encontrado.")
    exigir(feedback.id_reserva.isin(reservas.id_reserva).all(), "Feedback sem reserva.")
    exigir(reservas.categoria_hospedagem.isin(CATEGORIAS).all(), "Categoria incompatível.")
    exigir(reservas.status.isin({"realizada", "confirmada", "cancelada"}).all(), "Status inválido.")
    for coluna in ("n_viajantes", "valor_eur", "duracao_dias"):
        exigir(np.isfinite(reservas[coluna]).all() and reservas[coluna].gt(0).all(), f"Valor inválido: {coluna}")
    compra = pd.to_datetime(reservas.data_compra, format="%Y-%m-%d", errors="raise")
    viagem = pd.to_datetime(reservas.data_viagem, format="%Y-%m-%d", errors="raise")
    exigir(viagem.gt(compra).all() and compra.le(REFERENCIA).all(), "Datas de reserva incompatíveis.")
    exigir((viagem - compra).dt.days.eq(reservas.antecedencia_dias).all(), "Antecedência inconsistente.")
    exigir(feedback.nota_0_10.between(0, 10).all(), "Nota fora de escala.")
    ocupacao = tabelas["sintetico_ocupacao_hospedagens"]
    exigir(not ocupacao.duplicated(["data", "etapa", "categoria"]).any(), "Slot duplicado.")
    exigir(ocupacao.capacidade_vagas_noite.gt(0).all() and ocupacao.comprometidas_vagas_noite.ge(0).all(), "Capacidade inválida.")
    percentual = 100 * ocupacao.comprometidas_vagas_noite / ocupacao.capacidade_vagas_noite
    exigir(np.allclose(percentual, ocupacao.taxa_ocupacao_pct, atol=.051), "Taxa de ocupação inconsistente.")
    exigir(ocupacao.faltam_vagas_noite.eq((ocupacao.comprometidas_vagas_noite - ocupacao.capacidade_vagas_noite).clip(lower=0)).all(), "Déficit inconsistente.")
    financeiro = tabelas["sintetico_financeiro_mensal"]
    exigir(financeiro.contribuicao_brl.eq(financeiro.receita_contratada_brl - financeiro.custos_operacionais_brl).all(), "Contribuição inconsistente.")


def nps(notas: pd.Series) -> float | None:
    return None if notas.empty else float(100 * (notas.ge(9).sum() - notas.le(6).sum()) / len(notas))


def analisar(tabelas: dict[str, pd.DataFrame]) -> dict[str, Any]:
    validar(tabelas)
    reservas = tabelas["sintetico_reservas"]
    feedback, ocupacao = tabelas["sintetico_feedbacks_nps"], tabelas["sintetico_ocupacao_hospedagens"]
    respostas = pd.to_datetime(feedback.data_resposta, format="%Y-%m-%d", errors="raise")
    elegiveis = feedback.loc[respostas.le(REFERENCIA)]
    mensal = reservas.assign(mes=pd.to_datetime(reservas.data_viagem).dt.to_period("M").astype(str))
    mensal = mensal.loc[mensal.status.ne("cancelada")].groupby("mes", sort=True).agg(reservas=("id_reserva", "size"), viajantes=("n_viajantes", "sum"), valor_eur=("valor_eur", "sum")).reset_index()
    recorte = ocupacao.loc[ocupacao.data.eq("2026-11-14") & ocupacao.etapa.eq("Portomarín") & ocupacao.categoria.eq("Superior")].iloc[0]
    return {"natureza": "Simulação acadêmica complementar, seed 2026; independente da demo seed 42.",
            "referencia": "2026-11-16", "contagens": {nome: len(tabela) for nome, tabela in tabelas.items()},
            "reservas_por_status": {str(k): int(v) for k, v in reservas.status.value_counts().items()},
            "cancelamento_pct": float(100 * reservas.status.eq("cancelada").mean()),
            "nps_total": nps(feedback.nota_0_10), "respostas_total": len(feedback),
            "nps_ate_referencia": nps(elegiveis.nota_0_10), "respostas_ate_referencia": len(elegiveis),
            "respostas_futuras": int(respostas.gt(REFERENCIA).sum()),
            "ocupacao_agregada_pct": float(100 * ocupacao.comprometidas_vagas_noite.sum() / ocupacao.capacidade_vagas_noite.sum()),
            "deficit_vagas_noite": int(ocupacao.faltam_vagas_noite.sum()),
            "portomarin": {"data": "2026-11-14", "categoria": "Superior", "capacidade": int(recorte.capacidade_vagas_noite), "comprometidas": int(recorte.comprometidas_vagas_noite), "taxa_pct": float(recorte.taxa_ocupacao_pct)},
            "demanda_nao_cancelada": mensal.to_dict("records"),
            "fontes_externas": "Tabelas fornecidas: origem secundária, divergências entre séries e feriados calculados; não certificadas como estatísticas oficiais.",
            "limites": ["NPS 72 foi imposto no gerador: resultado do desenho, não descoberta.",
                        "Reservas usam EUR e categorias comerciais; financeiro usa BRL e é independente.",
                        "Ocupação não tem vínculo com reservas: não fazer joins por posição ou supor conciliação.",
                        "Registros chamados realizados se baseiam no início, não necessariamente na conclusão da viagem."]}


def executar() -> None:
    dados = analisar(carregar())
    PROCESSADOS.mkdir(parents=True, exist_ok=True)
    salvar_json(PROCESSADOS / "analise-suplementar.json", dados)
    print(json.dumps(dados, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    executar()
