# Pipeline do portfólio T4F

1. `src.ingestao`: verifica SHA-256 do snapshot e dos 18 arquivos originais incorporados.
2. `src.gerar_demo`: opcionalmente comprova geração seed 42 byte a byte, em diretório temporário.
3. `src.executar`: inicia uma única execução Node, com timeout, saída capturada e falhas explícitas. O adaptador `scripts/exportar-t4f.ts` chama os contratos e cálculos originais.
4. Núcleo TypeScript: Zod → PK/FK e invariantes → joins por mapas → coortes → KPIs, estatística e previsão.
5. Python reconcilia participações mensais, receitas por roteiro e composição da receita. Confere hash antes de gravar os artefatos.
6. Exporta sete CSVs e `analise-t4f.json` em `data/processed/`. Cada gravação usa arquivo temporário e replace. O JSON final é o contrato consumido pelas apresentações.
7. `src.visualizacoes`, `src.resultados`, `src.notebook` e `src.relatorio` produzem gráficos, narrativa, notebook executado e PDF.
8. `app.py` lê o JSON com cache pelo mtime; filtros escolhem visões por roteiro pré-calculadas. A aba de planejamento declara escopo global.

Não há ingestão remota em cada execução, dependência do checkout original, API ou banco operacional. As bibliotecas de apresentação não refazem o motor de previsão. O snapshot completo possui cerca de 356 KB; leitura única em memória é adequada. Estatística e modelos usam 34 pontos, sem necessidade de processamento distribuído.

## Falhas e consistência

O fluxo interrompe em erro de hash, schema, relações, subprocesso, timeout ou reconciliação. Não altera a fonte. As saídas são regeneráveis; a geração de vários arquivos não é uma transação de banco. Se uma execução for interrompida durante gravações, repetir todo o fluxo antes de publicar. Gráficos, notebook e PDF devem corresponder ao JSON final.

`src.pipeline`, `src.carregar_dados` e `src.analise` preservam a CLI de diagnóstico estrutural CSV genérica, sem misturar sua contagem de ausências com indicadores de negócio.
