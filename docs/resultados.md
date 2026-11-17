# Resultados T4F calculados

Dados sintéticos, seed 42; não representam desempenho real da Tour4Friends.

Histórico: janeiro/2024 a outubro/2026. Planejamento: 07/11 a 31/12/2026. Referência da base: 07/11/2026.

1. O mês 6 tem a maior média observada (10,7 viajantes; n=3), ante 0 no mês 1. Compare disponibilidade antes de ampliar vendas; são apenas 3 repetições do mês, sem comprovação inferencial de sazonalidade.

2. Assis apresenta a maior taxa observada entre roteiros com ao menos dez reservas: 21,4% (3/14), Wilson 95% 7,6–47,6%. Investigue motivos e canais; ranking descritivo não comprova diferença entre grupos.

3. Santiago a pé tem o menor NPS observado entre roteiros com 12 respostas: 25 (n=12). Hospedagem 7,1, atendimento 8,9 e logística 7,7 em dez pontos. Revise comentários; seleção de respondentes e amostra pequena impedem concluir causalidade ou diferença robusta.

4. Planejamento de 07/11 a 31/12/2026: ocupação de 43,86% (100/228 vagas-noite), com déficit de 4 vagas-noite em slots específicos. Negociar por saída/data/etapa/categoria; folga em outro slot não cobre a falta.

5. No histórico, receita contratada de R$ 1.618.600,00, custos de R$ 1.161.182,00 e contribuição de R$ 457.418,00. Não é lucro líquido: tributos, estornos e conciliação contábil não foram modelados.

6. Ridge temporal selecionado antes do teste final. MAE no holdout: 2,5567 viajantes/mês; RMSE 2,7508. A média ponderada teve menor MAE final; não se escolheu novamente o modelo após observar o teste.

## Rastreabilidade

Snapshot SHA-256: `b9362c92d4e8702eb685a532ee55dd7d9f21e2840ed10f652bad65e25fff237e`. Fontes e núcleo original em [fontes.json](fontes.json); contratos em [fontes-e-dicionario.md](fontes-e-dicionario.md). As conclusões são geradas por `python -m src.resultados`; tabelas em `data/processed/`.
