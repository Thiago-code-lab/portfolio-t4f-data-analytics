# Metodologias: evidências, adaptações e limites

| Abordagem | Aplicação demonstrável | Evidência | Limite |
| --- | --- | --- | --- |
| Panorama | Conectar contexto, atores, perguntas e decisões | problema.md e README | Sem entrevistas ou validação externa inventadas |
| CRISP-DM | Negócio/dados, preparação, modelos, avaliação e entrega | crisp-dm.md, pipeline, testes e artefatos | Entrega local; nenhum efeito operacional medido |
| KDD | Seleção, validação, transformação, descoberta e interpretação | kdd.md, tabelas, notebook | Descobertas sobre simulação, sem causalidade |
| Scrum | Histórico de incrementos no PI V e commits no portfólio | Git e PRs consultados | PDF p. 19 relata atividade Scrum; não comprova execução integral das cerimônias/quatro sprints |
| Kanban | Quadro de situação e critérios de aceite | planejamento.md | PDF p. 19 contém quadro Kanban; sem histórico de fluxo, WIP medido ou lead time |
| DataOps | Proveniência, hashes, contratos, testes e regeneração | fontes.json, lock npm, testes, verificacao.md | Sem CI ou operação produtiva deste portfólio |
| Planejamento | Etapas com dependências e aceite explícito | planejamento.md | Cotejo documental em leitura-documentacao.md, com propostas separadas de execução |
| Canvas | Proposta de valor, público, atividades, recursos e riscos | Canvas abaixo | Hipótese de valor acadêmica; não validada comercialmente |

## Canvas do portfólio

- **Problema:** informações de demanda, capacidade, experiência e finanças precisam ser interpretadas em conjunto.
- **Público:** gestores/analistas da agência no cenário, avaliador e leitores profissionais.
- **Valor:** processo analítico rastreável e decisões sugeridas com unidades, amostras e limites.
- **Recursos:** snapshot sintético público, núcleo original, Python, TypeScript, Git e computador local.
- **Atividades:** auditoria, seleção, validação, análise, avaliação e comunicação.
- **Entregas:** notebook, seis gráficos, leitor Streamlit, PDF e narrativa LinkedIn.
- **Sucesso verificável:** ao menos três análises calculadas, rastreabilidade, testes e concordância dos artefatos.
- **Custos:** estudo, execução local e dependências; sem custo de tokens ou inferência LLM.
- **Riscos:** confundir simulação com desempenho real, vagas-noite com viajantes, recebimentos com receita, ranking com causalidade e PR aberto com funcionalidade publicada.

## Conexão entre os elementos

A pergunta de capacidade nasce do problema da agência, usa slots e reservas validados, transforma participantes em comprometimento por slot e produz ocupação/déficit. O gráfico evidencia por que folga agregada não cobre falta localizada; a documentação propõe negociação por saída/data/etapa/categoria e registra o limite demonstrativo. O mesmo encadeamento aparece para demanda, experiência, cancelamentos e contribuição no notebook.

Não se atribui a criação destes documentos à adoção integral de todas as metodologias. Eles descrevem trabalho e evidência disponíveis; a documentação recebida foi cotejada por páginas em leitura-documentacao.md.
