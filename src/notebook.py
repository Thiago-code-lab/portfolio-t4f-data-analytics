"""Produz e executa a narrativa analítica com o Python do ambiente atual."""
import os
import asyncio
import sys
from pathlib import Path
from typing import Any

import nbformat as nbf
from ipykernel.kernelspec import install
from nbclient import NotebookClient

from src.config import RAIZ


def celulas() -> list[Any]:
    md, codigo = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
    inicio = ('from pathlib import Path\nimport sys\nimport pandas as pd\nfrom IPython.display import display, Markdown, Image\n'
              'RAIZ = Path.cwd()\nif RAIZ.name == "notebooks":\n    RAIZ = RAIZ.parent\n'
              'sys.path.insert(0, str(RAIZ))\nfrom src.resultados import carregar_resultados, insights\n'
              'from src.ingestao import verificar_fontes\nfrom src.executar import validar_resultado\n'
              'fontes = verificar_fontes()\ndados = carregar_resultados()\nvalidar_resultado(dados)\n'
              'assert fontes["dataset"]["sha256"] == dados["datasetSha256"]\n'
              'display(pd.DataFrame([dados["counts"]]))')
    return [md("# T4F Performance — portfólio analítico\n\nTour4Friends, Projeto Integrador V e Metodologias para Projetos de Big Data Analytics, Fatec Ipiranga. Dados sintéticos; nenhum resultado representa desempenho real. Pergunta: como integrar demanda, capacidade, experiência e contribuição para apoiar decisões?"),
            md("## Origem, contratos e reprodução\n\nSnapshot público da main integrada 0216dce; seed 42. Referência 07/11/2026, histórico completo jan/2024–out/2026. O gerador original é reexecutável; hashes em docs/fontes.json. Executar npm ci, instalar requirements.txt e rodar python -m src.executar. A validação Zod original verifica schemas, chaves, vínculos, datas e pagamentos; nenhum dado faltante é imputado silenciosamente."),
            codigo(inicio),
            md("## Demanda: distribuição e calendário\n\nParticipações confirmadas por mês de início da viagem, incluindo zeros conhecidos. Uma pessoa pode viajar mais de uma vez. Dois ou três anos por mês não provam sazonalidade. Negociar capacidade antes dos picos observados, sujeito a validação em novos períodos."),
            codigo('display(pd.DataFrame(dados["forecast"]["history"]))\ndisplay(pd.DataFrame(dados["seasonality"]["months"]))\ndisplay(Image(filename=str(RAIZ / "visualizacoes/demanda_sazonalidade.png")))'),
            md("## Cancelamentos e conversão\n\nCanceladas / todas as reservas da mesma coorte de viagem. Intervalos Wilson de referência binomial; clientes podem repetir, e rankings não demonstram diferenças. Conversão usa leads da coorte de primeiro contato com vínculo confirmado, uma população distinta. Comparar denominadores antes de decidir ações comerciais."),
            codigo('display(pd.DataFrame(dados["cancellations"]["groups"]))\ndisplay(Image(filename=str(RAIZ / "visualizacoes/cancelamentos.png")))'),
            md("## NPS e satisfação\n\nNPS em pontos = 100 × (promotores 9–10 − detratores 0–6) / respostas. Notas de hospedagem/atendimento/logística são dimensões distintas. Bootstrap original agrupa por cliente, 500 reamostragens, mínimo de 12 respostas e oito clientes; faixa exploratória não corrige viés de resposta."),
            codigo('display(pd.json_normalize(dados["satisfaction"]["groups"]))\ndisplay(Image(filename=str(RAIZ / "visualizacoes/satisfacao_nps.png")))'),
            md("## Capacidade: agregação não elimina gargalos\n\nPlanejamento global de 07/11 a 31/12/2026. Comprometimento vem das participações confirmadas por saída/categoria em cada slot de data/etapa. Vagas-noite não são viajantes/mês nem quantidade de hotéis. Déficit é somado após max(0, comprometimento − capacidade) por slot."),
            codigo('display(pd.DataFrame(dados["planning"]["slots"])[["routeName", "date", "category", "capacity", "committed", "shortage"]])\ndisplay(Image(filename=str(RAIZ / "visualizacoes/ocupacao_planejamento.png")))'),
            md("## Receita, custos e contribuição\n\nTotal da reserva conta uma vez; participantes não multiplicam a receita. Contribuição é receita contratada menos custos da coorte de saídas. Não é lucro líquido. Não somar receita a recebimentos. O cenário contém Assis e Espanha cultural além de Caminhos de Santiago; os registros não foram rebatizados."),
            codigo('display(pd.DataFrame(dados["historical"]["routes"])[["shortName", "travelers", "revenue", "cost", "contribution", "margin"]])\ndisplay(Image(filename=str(RAIZ / "visualizacoes/financeiro_roteiros.png")))'),
            md("## Previsão e avaliação temporal\n\nReuso integral do motor original: sazonal ingênuo, média ponderada, tendência amortecida e Ridge λ=4. Seleção H=3 em origens expansivas de jan/2024–abr/2026; holdout de mai–out/2026 separado. Futuro confirmado não entra no treino. Média ponderada venceu no teste final, sem reseleção. Faixas são exploratórias, sem garantia nominal; não há reconciliação hierárquica."),
            codigo('display(pd.DataFrame(dados["forecast"]["validation"]))\ndisplay(pd.DataFrame(dados["forecast"]["metrics"]))\ndisplay(Image(filename=str(RAIZ / "visualizacoes/previsao_demanda.png")))'),
            md("## Decisões, metodologias e limites\n\nCRISP-DM: problema → dados → preparação → análise/modelos → avaliação → entrega local. KDD: seleção do snapshot → validação → tabelas → descoberta exploratória → interpretação. Panorama e Canvas organizam problema e valor; planejamento e DataOps têm evidências em hashes, validações e artefatos. O documento acadêmico recebido descreve Scrum e contém quadro Kanban; isso não comprova a execução de todas as sprints. Ver docs/metodologias.md e docs/leitura-documentacao.md para o cotejo por página."),
            codigo('for texto in insights(dados):\n    display(Markdown(texto))'),
            md("## Base acadêmica complementar recebida\n\nO ZIP anexado é outra simulação, seed 2026: reservas em EUR e categorias Econômico/Standard/Superior. Não unir à demo seed 42 em BRL, Premium/Conforto/Alternativa. Ocupação e financeiro são independentes de reservas. NPS 72 foi imposto no gerador. As tabelas com prefixo real_ têm origem secundária ou calendário calculado, sem certificação primária nesta entrega."),
            codigo('import json\nsuplementar = json.loads((RAIZ / "data/processed/analise-suplementar.json").read_text(encoding="utf-8"))\ndisplay(pd.DataFrame([suplementar["contagens"]]))\ndisplay(pd.DataFrame([{chave: suplementar[chave] for chave in ("nps_total", "respostas_total", "nps_ate_referencia", "respostas_ate_referencia", "respostas_futuras")}]))\ndisplay(pd.DataFrame([suplementar["portomarin"]]))\nassert suplementar["portomarin"]["taxa_pct"] == 150\nassert suplementar["respostas_futuras"] == 7'),
            md("## Próximos passos\n\nValidar indicadores com novos períodos e dados operacionais autorizados; conferir as fontes externas primárias antes de uso comercial. O relatório acadêmico foi incluído como referência documental, com matrículas ocultadas e divergências técnicas explicitadas. Este portfólio é publicado no GitHub; Streamlit permanece uma execução local. Fonte: https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/tree/0216dce5f67b83fbb0ba84346a7742dcb4f5ce23 .")]


def executar() -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    install(prefix=sys.prefix, kernel_name="t4f-portfolio", display_name="Python (T4F Portfólio)")
    os.environ["JUPYTER_PATH"] = str(Path(sys.prefix) / "share/jupyter") + os.pathsep + os.environ.get("JUPYTER_PATH", "")
    notebook = nbf.v4.new_notebook(cells=celulas())
    notebook.metadata.kernelspec = {"display_name": "Python (T4F Portfólio)", "language": "python", "name": "t4f-portfolio"}
    NotebookClient(notebook, timeout=90, kernel_name="t4f-portfolio", resources={"metadata": {"path": str(RAIZ)}}).execute()
    nbf.write(notebook, RAIZ / "notebooks/analise_exploratoria.ipynb")


if __name__ == "__main__":
    executar()
