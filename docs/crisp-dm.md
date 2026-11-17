# CRISP-DM no T4F

| Fase | Execução nesta entrega | Evidência |
| --- | --- | --- |
| Entendimento de negócio | Problema, público e decisões propostas | problema.md |
| Entendimento dos dados | Snapshot, dez coleções, chaves, unidades, coortes e limites | fontes-e-dicionario.md e fontes.json |
| Preparação | Verificação de hash, schemas e relações; recorte histórico separado de futuro | src/ingestao.py, núcleo original e exportar-t4f.ts |
| Modelagem | Indicadores descritivos, Wilson/bootstrap exploratórios e quatro candidatos de previsão | vendor/t4f/src/lib e JSON analítico |
| Avaliação | Carteira manual, reconciliação, validação temporal anterior ao holdout e testes | tests, notebook e verificacao.md |
| Entrega | Tabelas, gráficos, leitor, PDF e texto profissional | visualizacoes, output/pdf e portfolio |

A preparação valida dados gerados e não alega limpeza de erros inexistentes. A avaliação distingue validação para escolha do modelo e teste final; não seleciona novamente o método pelo teste. A entrega é local e não demonstra adoção operacional na Tour4Friends. Cotejo com a documentação acadêmica recebida em leitura-documentacao.md; propostas e execução distinguidas.
