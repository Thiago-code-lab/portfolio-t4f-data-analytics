# KDD: seleção até interpretação

1. **Seleção:** snapshot público synthetic_demo da main integrada; exclusão de documentos comerciais e branches pendentes. Histórico e planejamento separados.
2. **Pré-processamento:** hashes, tipos, enums, datas, duplicidade, PK/FK, participantes e pagamentos. Erros são recusados; não há imputação ou perdas de registros alegadas sem evidência.
3. **Transformação:** relações por ID, coortes temporais, demanda mensal com zeros conhecidos, receita por reserva e comprometimento por slot. Tabelas CSV e JSON com reconciliação.
4. **Descoberta:** calendário da demanda, cancelamentos, NPS, capacidade e contribuição; modelos de previsão originais com avaliação temporal. Não se inventam anomalias para tornar a narrativa mais atraente.
5. **Interpretação:** números, unidades, amostras e decisões propostas no notebook, gráficos e resultados; limites sintéticos explícitos.

Evidências: fontes.json, scripts/exportar-t4f.ts, vendor/t4f/src/lib, tests, docs/resultados.md e notebook executado. A base não fundamenta conclusões causais ou resultados reais da agência. Documento acadêmico recebido e relacionado por páginas em leitura-documentacao.md.
