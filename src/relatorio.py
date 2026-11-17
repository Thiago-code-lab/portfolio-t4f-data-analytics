"""Relatório de portfólio calculado, com páginas e fontes explícitas."""
from html import escape
import json
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.config import COMMIT_ORIGINAL, RAIZ
from src.resultados import carregar_resultados, formatar, insights

ESTILOS = getSampleStyleSheet()


def configurar() -> None:
    fontes = Path("C:/Windows/Fonts")
    if (fontes / "arial.ttf").exists():
        pdfmetrics.registerFont(TTFont("Portfolio", str(fontes / "arial.ttf")))
        pdfmetrics.registerFont(TTFont("PortfolioBold", str(fontes / "arialbd.ttf")))
    else:
        from matplotlib import font_manager
        pdfmetrics.registerFont(TTFont("Portfolio", font_manager.findfont("DejaVu Sans")))
        pdfmetrics.registerFont(TTFont("PortfolioBold", font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold"))))
    ESTILOS.add(ParagraphStyle(name="CorpoT4F", fontName="Portfolio", fontSize=10, leading=15, spaceAfter=10, textColor=colors.HexColor("#263b50")))
    for nome in ("Title", "Heading1", "Heading2"):
        ESTILOS[nome].fontName = "PortfolioBold"
        ESTILOS[nome].textColor = colors.HexColor("#175d78")
        ESTILOS[nome].spaceAfter = 14


def texto(conteudo: str) -> Paragraph:
    return Paragraph(escape(conteudo), ESTILOS["CorpoT4F"])


def imagem(nome: str, altura: float = 210) -> Image:
    return Image(str(RAIZ / "visualizacoes" / nome), width=500, height=altura, kind="proportional")


def titulo(conteudo: str) -> list[Flowable]:
    return [PageBreak(), Paragraph(conteudo, ESTILOS["Heading1"])]


def rodape(canvas: Any, documento: Any) -> None:
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cedee5"))
    canvas.line(44, 40, A4[0] - 44, 40)
    canvas.setFont("Portfolio", 8)
    canvas.setFillColor(colors.HexColor("#536579"))
    canvas.drawString(44, 27, "T4F Performance | Portfólio analítico | Dados sintéticos")
    canvas.drawRightString(A4[0] - 44, 27, str(documento.page))
    canvas.restoreState()


def abertura(dados: dict[str, Any]) -> list[Flowable]:
    historico = dados["historical"]
    tabela = Table([["Histórico jan/2024-out/2026", "Resultado demonstrativo"],
                    ["Participações confirmadas", str(historico["travelers"])],
                    ["Reservas da coorte / confirmadas", f"{historico['bookings']} / {historico['confirmed']}"],
                    ["NPS / respostas", f"{formatar(historico['nps'])} pontos / {historico['responses']}"],
                    ["Contribuição gerencial", f"R$ {formatar(historico['contribution'])}"]], colWidths=[295, 205])
    tabela.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e4f0f3")),
                               ("FONTNAME", (0, 0), (-1, 0), "PortfolioBold"),
                               ("FONTNAME", (0, 1), (-1, -1), "Portfolio"),
                               ("FONTSIZE", (0, 0), (-1, -1), 9),
                               ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    return [Spacer(1, 25), Paragraph("T4F Performance", ESTILOS["Title"]),
            texto("Tour4Friends | Portfólio de Data Analytics | 17/11/2026"),
            texto("Fatec Ipiranga - Metodologias para Projetos de Big Data Analytics. Professor Samuel Henrique. Organização do portfólio: Thiago Cardoso Davi."),
            Paragraph("Do problema de negócio às evidências", ESTILOS["Heading1"]),
            texto("A Tour4Friends organiza roteiros do Caminho de Santiago para peregrinos brasileiros. O Projeto Integrador V desenvolveu uma solução de inteligência de negócios para conectar demanda, reservas, hospedagens, ocupação, experiência, finanças e previsões."),
            texto("Este portfólio demonstra o processo analítico sobre a base sintética reproduzível do projeto. Não duplica a aplicação nem apresenta os números como desempenho real da agência. O cenário preserva também roteiros demonstrativos de Assis e Espanha cultural."),
            tabela, Spacer(1, 20),
            texto("Projeto Integrador V: Daniel Fernando dos Santos; Lucas Antonio Evangelista dos Santos; Pablo Roberto da Silva Costa; Thiago Cardoso Davi; William Nunes Vilany."),
            texto("A entrega relaciona problema, dados, pipeline, análise, visualizações e metodologias. A documentação acadêmica do grupo, recebida em 17/11/2026, foi cotejada com o software executável. O ZIP complementar e uma cópia pública do documento estão incluídos, com distinções de escopo e proteção das matrículas.")]


def dados_e_pipeline(dados: dict[str, Any]) -> list[Flowable]:
    return titulo("1. Dados, contratos e pipeline") + [
        texto(f"Origem: repositório público Dashboards-Tour4Friends, commit integrado {COMMIT_ORIGINAL}. Snapshot public/data/demo.json, seed 42, versão 1.0.0. Referência: 07/11/2026. Histórico completo: 01/01/2024 a 31/10/2026. Valores em BRL demonstrativos."),
        texto("Base completa: 116 clientes fictícios, 164 reservas, 258 leads, seis roteiros, 52 saídas, 12 hospedagens demonstrativas, 609 slots, 156 custos, 147 pagamentos e 72 avaliações. Slot é uso de hospedagem por saída/data/etapa/categoria; não representa um hotel distinto."),
        Paragraph("Fluxo reproduzível", ESTILOS["Heading2"]),
        texto("1. Verificar SHA-256 do snapshot e dos 18 arquivos incorporados do núcleo original. 2. Validar schemas e relações com Zod. 3. Construir visões e calcular indicadores/modelos no TypeScript original. 4. Reconciliar totais em Python. 5. Exportar sete CSVs e JSON. 6. Gerar seis PNGs, notebook executado, narrativa e PDF. O Streamlit apenas lê os agregados."),
        texto("Entradas inconsistentes são recusadas: chaves duplicadas, referências inexistentes, datas incompatíveis, pagamentos acima do contratado e origem diferente de synthetic_demo. Não há imputação nem tentativa silenciosa de corrigir valores. A limpeza neste caso é verificação de contrato sobre uma base gerada e controlada."),
        Paragraph("Unidades e coortes", ESTILOS["Heading2"]),
        texto("Demanda: participações confirmadas por mês da viagem, incluindo meses conhecidos sem movimento. Reserva: valor total contado uma vez, sem multiplicar por viajantes. Conversão: leads por primeiro contato com reserva confirmada vinculada. Feedback: respostas vinculadas à coorte histórica, com corte temporal. Ocupação: comprometimento / capacidade dos mesmos slots, em vagas-noite."),
        texto("Histórico e planejamento são recortes separados. Planejamento termina em dezembro/2026; a saída de janeiro/2027 continua no snapshot, fora desse recorte. Custo por categoria, no original, é rateio por receita; não equivale a custo individual apurado."),
        texto("SHA-256 do snapshot: " + dados["datasetSha256"]),
        texto("Performance: leitura local única, validação e joins por mapas no núcleo, série de 34 meses e sistema Ridge 6 x 6. Sem LLM, APIs pagas, treinamento redundante ou banco operacional nesta reprodução. Fontes e contratos: docs/fontes.json e docs/fontes-e-dicionario.md.")]


def analises(dados: dict[str, Any]) -> list[Flowable]:
    narrativas = insights(dados)
    return titulo("2. Demanda e calendário") + [
        texto("Decisão apoiada: quando investigar picos e antecipar negociação de capacidade, antes de ampliar vendas."),
        imagem("demanda_sazonalidade.png", 245), texto(narrativas[0]),
        texto("A série reúne 188 participações confirmadas em 34 meses. Meses sem viagens são zeros conhecidos da simulação. Repetições da mesma pessoa e poucas observações por mês limitam conclusões; o padrão descritivo não prova sazonalidade comercial real."),
        texto("Indicadores e tabela de origem: data/processed/demanda_mensal.csv e sazonalidade.csv; contrato e cálculo no núcleo original versionado.")]


def experiencia(dados: dict[str, Any]) -> list[Flowable]:
    narrativas = insights(dados)
    return titulo("3. Experiência e cancelamentos") + [
        imagem("satisfacao_nps.png", 195), texto(narrativas[2]),
        imagem("cancelamentos.png", 195), texto(narrativas[1]),
        texto("Ações propostas: revisar comentários e etapas de hospedagem; investigar motivos e canais de cancelamento. O NPS usa promotores 9-10 e detratores 0-6. O núcleo calcula bootstrap exploratório por cliente com 500 reamostragens, mínimo de 12 respostas e oito clientes. Wilson é referência binomial com independência imperfeita. Nenhum ranking prova causalidade. Tabelas: satisfacao.csv e cancelamentos.csv.")]


def capacidade_financas(dados: dict[str, Any]) -> list[Flowable]:
    narrativas = insights(dados)
    return titulo("4. Capacidade e contribuição") + [
        imagem("ocupacao_planejamento.png", 195), texto(narrativas[3]),
        imagem("financeiro_roteiros.png", 195), texto(narrativas[4]),
        texto("Decisões apoiadas: contratar nos slots em falta e revisar composição de receita/custos por roteiro. Folgas de outras datas não são transferíveis. Não somar recebimentos a receita; não subtrair vagas-noite de viajantes/mês. Tabelas: ocupacao_planejamento.csv e roteiros.csv.")]


def modelos(dados: dict[str, Any]) -> list[Flowable]:
    modelo = dados["forecast"]
    validacao = next(linha for linha in modelo["validation"] if linha["modelId"] == modelo["selectedId"] and linha["horizon"] == 3)
    teste = next(linha for linha in modelo["metrics"] if linha["modelId"] == modelo["selectedId"])
    ponderada = next(linha for linha in modelo["metrics"] if linha["modelId"] == "weighted")
    return titulo("5. Previsão e avaliação temporal") + [
        imagem("previsao_demanda.png", 230), texto(insights(dados)[5]),
        texto("Quatro candidatos: sazonal ingênuo, média ponderada, tendência amortecida e Ridge temporal com lambda 4. Origens expansivas no desenvolvimento até abril/2026 selecionam em H=3; maio-outubro/2026 permanece como teste final de seis meses. O método é congelado antes de avaliar esse teste."),
        texto(f"MAE de validação H=3: {formatar(validacao['mae'], 4)}, em {validacao['windows']} origens. No teste final, MAE {formatar(teste['mae'], 4)}, RMSE {formatar(teste['rmse'], 4)} e viés {formatar(teste['bias'], 4)}. A média ponderada obteve MAE {formatar(ponderada['mae'], 4)} no teste, sem reseleção oportunista. Valores calculados pelo núcleo original."),
        texto(f"Faixas exploratórias: {modelo['uncertainty']['coverage']['hits']}/{modelo['uncertainty']['coverage']['count']} alvos do holdout cobertos; não há garantia de cobertura futura. Quantis vêm dos erros de validação, não do teste final. Confirmados futuros não entram no treino."),
        texto("Série curta e snapshot atual de status, sem fotografias históricas de reservas conhecidas em cada data. Recortes esparsos podem usar fallback explícito. Nenhuma anomalia ultrapassou os critérios originais; não reduzir limiares para fabricar achados. Previsão não cria reservas ou contratos de hospedagem.")]


def metodos() -> list[Flowable]:
    return titulo("6. Metodologias, evidências e próximos passos") + [
        texto("Panorama: problema, atores, dados, decisões e limites conectados no README. CRISP-DM: entendimento do negócio/dados, preparação, modelagem, avaliação e entrega local mapeados aos artefatos. KDD: seleção do snapshot, validação, transformação em tabelas, descoberta e interpretação exploratória."),
        texto("DataOps: hashes, origem imutável, dependências fixadas, validações, testes e geração reproduzível. Planejamento e Canvas: problema, público, recursos, entregas e riscos. O documento acadêmico descreve atividade Scrum e apresenta quadro Kanban na página 19 e Canvas na página 23. Esses registros não demonstram todas as cerimônias ou quatro sprints executadas; não são declaradas métricas de fluxo."),
        texto("Validação: carteira manual independente com quatro recortes; testes de entradas malformadas, relações, pagamentos, ausência de amostra, futuro fora do treino, geração byte a byte e reconciliação de totais. Sete testes CSV genéricos preservados. Ver docs/verificacao.md para os resultados executados nesta migração; não confundir com os testes históricos do Projeto Integrador V."),
        texto("Estado do original: PRs 1-3 integrados; PRs 4-8 abertos, sendo 6-8 em rascunho na consulta de 17/11/2026. A referência do portfólio é a main 0216dce. Catálogo comercial, documentos de tarifas, WIP de hospedagens e mapas pendentes não foram incorporados. O original foi consultado apenas em leitura."),
        texto("Limitações: dados sintéticos, composição pequena, NPS com viés de resposta, intervalos exploratórios, status retroativos, ausência de conciliação contábil e de dados operacionais autorizados. Não há evidência de ganho financeiro real, causalidade ou market share. O documento acadêmico recebido não comprova a execução de Random Forest, Regressão Logística, Power BI ou automação semanal neste repositório; essas propostas ficam distinguidas da implementação."),
        Paragraph("Reprodução e referências", ESTILOS["Heading2"]),
        texto("README: instalar requirements.txt e npm ci; executar src.executar, src.visualizacoes, src.resultados, src.notebook e src.relatorio. Streamlit: python -m streamlit run app.py. As tabelas, gráficos e textos derivam do mesmo snapshot."),
        Paragraph('<link href="https://github.com/Thiago-code-lab/Dashboards-Tour4Friends">Projeto Integrador V: Dashboards-Tour4Friends</link>. Código e documentação pública, commit 0216dce. Contratos: src/types/domain.ts; KPIs: docs/kpis.md; modelos: docs/model-validation.md; estatística: docs/statistical-analysis.md. Consulta: 17/11/2026.', ESTILOS["CorpoT4F"]),
        texto("Destino público autorizado: github.com/Thiago-code-lab/portfolio-t4f-data-analytics. O leitor Streamlit é local; não há hospedagem web ou postagem automática no LinkedIn. Fontes externas secundárias e dados operacionais exigem validação adicional antes de decisões reais.")]


def anexos() -> list[Flowable]:
    dados = json.loads((RAIZ / "data/processed/analise-suplementar.json").read_text(encoding="utf-8"))
    return titulo("7. Documentação e base complementar") + [
        texto("Documento acadêmico do grupo: Análise de dados aplicada ao Caminho de Santiago, 30 páginas. Cópia pública em docs/referencias/projeto-big-data-t4f-publico.pdf, com dez matrículas ocultadas; texto e figuras preservados. O original permanece local e não é publicado."),
        texto("Leitura por páginas: 7-12, problema, dados, pipeline e insight; 13-18, Panorama, CRISP-DM e KDD; 19, Scrum e Kanban; 20-22, DataOps e planejamento; 23, Canvas. As propostas de modelos/infraestrutura e metas ilustrativas não são apresentadas como funcionalidades já executadas. O modelo de repositório de outro domínio na página 28 não foi adotado."),
        texto("Pacote original fornecido: anexos/bases_de_dados_T4F.zip, contendo nove CSVs, planilha de dez abas, LEIA-ME e gerador. Arquivo preservado byte a byte e inspecionado; não contém histórico transacional privado da agência. Os CSVs foram extraídos e validados separadamente em data/suplementar."),
        texto("São 422 perfis fictícios, 469 reservas, 300 feedbacks, 4.662 slots e sete registros financeiros, além de quatro tabelas externas de referência. A simulação seed 2026 usa categorias Econômico, Standard e Superior e valores de reservas em EUR. Não se une à demonstração seed 42 em BRL. Ocupação e financeiro não têm chave conciliável com reservas."),
        texto(f"Qualidade temporal: NPS total {formatar(dados['nps_total'])} em {dados['respostas_total']} respostas, imposto pelo gerador. Há {dados['respostas_futuras']} respostas posteriores a 16/11/2026; no corte, restam {dados['respostas_ate_referencia']} e NPS {formatar(dados['nps_ate_referencia'])}. Não interpretar o total como uma medição histórica independente."),
        texto("Caso do documento reproduzido: Portomarín, 14/11/2026, categoria Superior, três vagas-noite comprometidas para duas de capacidade: 150% e uma vaga-noite em falta. A decisão sugerida é negociar a falta localizada; não supor que capacidade de outro dia a cobre."),
        texto("As séries externas usam fontes secundárias e o calendário é calculado. Há números divergentes de brasileiros por caminho entre as fontes fornecidas; não somar versões concorrentes, nem certificar os dados como oficiais. O percentual de 60,5% é reprodução do recorte apresentado no documento, não participação de mercado da agência ou validação de um modelo."),
        texto("Rastreabilidade: docs/anexos-manifesto.json, docs/leitura-documentacao.md e docs/bases-suplementares.md. Reprodução independente: python -m src.suplementar. O notebook inclui contagens, corte temporal e o caso de capacidade.")]


def executar() -> None:
    configurar()
    dados = carregar_resultados()
    destino = RAIZ / "output/pdf/portfolio-t4f-performance.pdf"
    destino.parent.mkdir(parents=True, exist_ok=True)
    documento = SimpleDocTemplate(str(destino), pagesize=A4, rightMargin=44, leftMargin=44,
                                  topMargin=38, bottomMargin=54, title="T4F Performance - Portfólio de Data Analytics", author="Thiago Cardoso Davi")
    documento.build(abertura(dados) + dados_e_pipeline(dados) + analises(dados) + experiencia(dados)
                    + capacidade_financas(dados) + modelos(dados) + metodos() + anexos(), onFirstPage=rodape, onLaterPages=rodape)


if __name__ == "__main__":
    executar()
