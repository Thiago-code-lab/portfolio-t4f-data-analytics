# Problema de negócio e panorama

A Tour4Friends organiza roteiros do Caminho de Santiago para peregrinos brasileiros. Planejar demanda, reservas e hospedagens exige cruzar comercial, capacidade por data/etapa, experiência e finanças. Um total agregado pode esconder falta de vagas ou diferenças de experiência.

**Pergunta central:** como conectar esses indicadores para orientar investigação e planejamento, mantendo origem, unidades, coortes e limitações explícitas?

| Pergunta | Dado e cálculo | Visualização | Decisão apoiada |
| --- | --- | --- | --- |
| Quando se concentram as viagens? | Participações confirmadas por mês; zeros conhecidos | demanda_sazonalidade.png | Antecipar investigação/negociação de capacidade |
| Onde rever a experiência? | NPS, respostas e notas por dimensão | satisfacao_nps.png | Ler feedbacks e revisar etapas |
| Onde investigar cancelamentos? | Canceladas / todas as reservas por roteiro e Wilson | cancelamentos.png | Investigar motivos e canais |
| Há capacidade nas datas certas? | Comprometimento e falta por slot | ocupacao_planejamento.png | Negociar no slot deficitário |
| Como se compõe a contribuição? | Receita contratada − custos da coorte | financeiro_roteiros.png | Rever composição de custos/receita |
| A previsão supera uma referência simples? | Validação temporal e holdout | previsao_demanda.png | Avaliar uso cauteloso no planejamento |

Público: gestores e analistas, avaliador acadêmico e leitores profissionais do portfólio. Panorama conecta problema → snapshot sintético → contratos → indicadores → gráficos → decisões propostas.

Escopo: estudo demonstrativo reproduzível e documentação do desenvolvimento do T4F no PI V. Histórico jan/2024–out/2026; planejamento 07/11–31/12/2026. Não há decisões automatizadas, integração operacional, alegação de resultados reais ou entrevistas inventadas. O cenário original contém seis roteiros, inclusive Assis e Espanha cultural; preservamos a base e explicitamos essa abrangência.
