# Visualizações T4F verificáveis

Geradas por python -m src.visualizacoes a partir de data/processed/analise-t4f.json:

1. demanda_sazonalidade.png — série mensal e calendário, histórico jan/2024–out/2026.
2. cancelamentos.png — taxa por roteiro com denominador e Wilson.
3. satisfacao_nps.png — NPS em pontos, com tamanho da amostra.
4. ocupacao_planejamento.png — capacidade, comprometimento e falta por slot, 07/11–31/12/2026.
5. financeiro_roteiros.png — receita, custos e contribuição, histórico.
6. previsao_demanda.png — histórico, projeção original e faixa exploratória.

Todos usam o snapshot sintético seed 42. Os PNGs são entregas versionadas; decisões e limites em docs/resultados.md. Não são capturas fabricadas nem evidência de desempenho real.
