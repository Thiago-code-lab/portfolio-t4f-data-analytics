# Leitura da documentação acadêmica recebida

Documento fornecido pelo autor em 17/11/2026: **Análise de dados aplicada ao Caminho de Santiago**, 30 páginas. [Cópia pública](referencias/projeto-big-data-t4f-publico.pdf). Não é um enunciado do professor: é o trabalho acadêmico do grupo, com metodologia, figuras, propostas e relatos. Dez números de matrícula foram ocultados; texto, autoria e figuras foram preservados. O original permanece fora do material público.

| Páginas | Elemento documental | Tratamento no portfólio |
| --- | --- | --- |
| 1–2 | Instituição, integrantes e orientação | Créditos mantidos; matrículas ocultadas |
| 4–5 | Resumo e abstract com infraestrutura e modelos | Relato do documento, não prova de execução |
| 7–8 | Contexto Tour4Friends, fragmentação e capacidade | Problema e decisão conectados aos dados e gráficos |
| 9 | Fontes públicas, privadas e sintéticas | Base privada não incluída; fontes secundárias qualificadas |
| 10 | Pipeline semanal, banco, modelos e alertas | Proposta/relato: não há implementação comprovada dessa automação neste repositório |
| 11–12 | Recorte de chegadas e 60,5% nos caminhos portugueses | Aritmética do recorte: (3.317 + 1.225) / (3.317 + 1.225 + 2.968) = 60,48%; fonte primária exata não certificada aqui |
| 13–14 | Panorama | Problema, atores, dados e valor ligados ao README |
| 15–16 | CRISP-DM, Logística e Random Forest | Modelos propostos no documento; motor executável usa quatro candidatos temporais, sem alegar equivalência |
| 17–18 | KDD | Seleção, preparação, transformação e interpretação ligadas aos artefatos |
| 19 | Relato de atividade Scrum, link de vídeo e figura Kanban | Evidência documental recebida; cerimônias e quatro sprints não verificadas independentemente |
| 20–22 | DataOps e planejamento | Distinguir automação/Power BI propostos das validações e execução local implementadas |
| 23 | Canvas e início do projeto final | Canvas documental e proposta de valor relacionados ao caso |
| 24–25 | Relato de resultados/implantação | Não usar como prova de modelo treinado ou ganho real sem artefatos |
| 26–27 | Texto LinkedIn | Mantido como referência; versão publicável evita alegações de execução não demonstradas |
| 28–29 | Modelo genérico de GitHub de outro domínio | Não adotado como estrutura ou README deste projeto |
| 29–30 | Conclusões, metas e roadmap | Metas de ocupação/F1 são ilustrativas; não resultados medidos |

## Distinções técnicas

O PDF fala de Regressão Logística, Random Forest, Power BI, banco central, execução semanal e e-mail. O código reproduzido aqui comprova validação de snapshot, indicadores descritivos, Wilson/bootstrap exploratórios e previsão temporal (sazonal, ponderada, amortecida e Ridge). Não há código, configuração de agendador, relatório de treinamento ou arquivo Power BI que comprove as demais alegações neste portfólio.

F1 é métrica de classificação, não substitui MAE/RMSE para previsão numérica de viajantes. Nenhum ganho de 10% de ocupação ou F1 de 0,70 foi declarado atingido. O cenário de captura de 0,5% do documento é premissa, não participação de mercado comprovada.

No ZIP, o exemplo de Portomarín é reproduzível, mas reservas, ocupação e financeiro não formam uma base transacional conciliada. O NPS 72 é uma construção do gerador. Os sete feedbacks futuros em relação a 16/11/2026 foram contados separadamente, sem apagar a fonte. Ver [bases complementares](bases-suplementares.md).
