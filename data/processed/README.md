# Artefatos analíticos regeneráveis

python -m src.executar publica analise-t4f.json e sete CSVs: demanda_mensal, roteiros, sazonalidade, cancelamentos, satisfacao, previsoes e ocupacao_planejamento.

Tabelas e JSON ficam fora do Git e são reconstruídos a partir do snapshot versionado. As apresentações leem o JSON final; contratos e recortes estão em docs/fontes-e-dicionario.md. Se uma execução for interrompida, repetir o fluxo completo antes de publicar.
