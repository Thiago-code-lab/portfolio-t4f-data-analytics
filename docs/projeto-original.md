# Projeto original: arquitetura, evidências e estado

Consulta em 17/11/2026. Origem: [Dashboards-Tour4Friends](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends). O projeto original foi localizado e confirmado por seu remoto, depois consultado somente em leitura, inclusive arquivos, histórico, branches e status; nenhum checkout, instalação, geração ou teste foi executado nele.

## Referência e publicação

Checkout encontrado: `feature/hospedagens-comparacao-03`, HEAD `58b05df`, com dez arquivos rastreados modificados e arquivos não rastreados. O WIP inclui comparação de hospedagens e documentos comerciais; não foi copiado. A worktree de evolução do professor também não foi alterada.

A `main` local e a consulta `git ls-remote` apontam para `0216dce5f67b83fbb0ba84346a7742dcb4f5ce23`. Essa é a referência imutável usada, extraída com `git show`, não a branch ativa. O README antigo ainda dizia “candidata”, mas seu texto não supera a evidência dos merges.

| PR | Tema | Estado confirmado no GitHub |
| --- | --- | --- |
| [#1](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/pull/1) | Backend autenticado/PostgreSQL | Integrado em main, merge 0216dce |
| [#2](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/pull/2) | Analytics e validação temporal | Integrado na cadeia, merge 55e06d7 |
| [#3](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/pull/3) | Qualidade e entrega | Integrado na cadeia, merge ff1ff25 |
| [#4](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/pull/4) | Catálogo e orçamento 2027 | Aberto |
| [#5](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/pull/5) | Roteiros documentais | Aberto, base #4 |
| [#6](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/pull/6) | KPIs percentuais e contribuição | Aberto em draft |
| [#7](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/pull/7) | Filtros por caminho e KPIs | Aberto em draft, base #5 |
| [#8](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/pull/8) | Mapa e cenário de demanda | Aberto em draft, base #7 |

[Evidência normalizada do conector GitHub](estado-original.json). Consulta HTTP ao Pages e ao JSON público retornou 200 e SHA-256 idêntico ao snapshot incorporado, em [verificacao-publica.json](verificacao-publica.json). Não se conclui que o backend esteja hospedado: o Pages é estático e o laboratório é separado. Não foram repetidos os testes completos na URL pública nesta migração.

## Arquitetura

React 19, TypeScript, Vite, Tailwind 4, HashRouter, Recharts e Zod. Páginas secundárias usam carregamento sob demanda; provider central compartilha snapshot validado e agregações memoizadas. Adaptadores `StaticDataRepository` e `ApiDataRepository` separam demo e API. Sessão de laboratório fica em memória e o retorno à demo é explícito.

FastAPI, Pydantic v2, SQLAlchemy assíncrono, Psycopg 3, Alembic e PostgreSQL no laboratório. Migração, seed idempotente, quatro perfis, CRUD com versão esperada, auditoria e importação transacional. O portfólio não requer banco ou credenciais.

## Fontes, geração e importação

`scripts/generate_demo_data.py` gera `public/data/demo.json` com seed 42 e timestamp fixo. O contrato em `src/types/domain.ts` define dez coleções e metadados synthetic_demo. `src/lib/validation/dataset.ts` verifica schemas, PK/FK, relações comerciais, datas, capacidade e pagamentos.

A aplicação aceita importação CSV segundo o contrato demonstrativo: merge por ID, validação global antes de substituir o estado. O backend faz validação e commit separados por token descartável, hash do lote e versões; não se trata de integração operacional da agência. O portfólio usa apenas o snapshot público e não importa planilhas ou documentos comerciais.

## Dez módulos da referência integrada

| Módulo | Indicadores e decisões |
| --- | --- |
| Visão geral | Reservas, participações, receita, NPS, ocupação, alertas e insights |
| Demanda e previsões | Série, quatro candidatos, validação temporal, simulador e estatística |
| Reservas e comercial | Funil, conversão por coorte, pipeline, status e canais |
| Roteiros e destinos | Volume, receita, custos, contribuição e categorias |
| Hospedagens e capacidade | Slots de data/etapa/categoria, comprometimento e déficits |
| Operações e alertas | Seis regras, causa, ação e revisão do alerta |
| Experiência do cliente | NPS, amostra, distribuição e notas por dimensão |
| Financeiro | Receita contratada/realizada, pagamentos, custos e contribuição |
| Relatório executivo | Documento imprimível com resumo, gráficos e métodos |
| Sobre e metodologia | KPIs, origem, arquitetura, qualidade e limitações |

O catálogo dos PRs seguintes é um incremento separado; não substituir os dez módulos por uma contagem que inclua trabalho ainda aberto.

## Análises e modelos existentes

Sazonalidade descritiva com zeros conhecidos, cancelamentos e Wilson, satisfação com bootstrap por cliente (500 reamostragens) e anomalias robustas por MAD/IQR com abstenção sem amostra. Alertas operacionais são regras distintas de anomalias estatísticas; zero anomalias na base não significa ausência de alertas.

Motor: sazonal ingênuo, média ponderada de três meses, Holt amortecido e Ridge temporal lambda 4, sistema 6 × 6. Seleção por MAE em H=3, origens expansivas antes do holdout de seis meses; preferência por simplicidade dentro de 1%. Métricas MAE/RMSE/viés/WAPE e quantis de resíduos por passo. Fallback e critérios de elegibilidade explícitos. Futuro confirmado não integra treino; não há reconciliação hierárquica.

## Testes e evidências disponíveis

Foram inspecionados testes Vitest de dados, KPIs, capacidade, previsão e estatística; fixture independente com resultados manuais; testes de API e E2E Playwright; backend com Pytest/PostgreSQL e paridade TypeScript/Python. Documentos da referência registram 95 Vitest, 27 Pytest e oito testes conectados; há também evidências históricas de navegação, acessibilidade e PDF. Esses números são **registros do original**, não testes executados nesta migração. Evidências locais do portfólio estão em [verificacao.md](verificacao.md).

A reprodução do portfólio incorpora apenas 18 arquivos puros, o JSON e as fixtures necessárias, com atribuição em [vendor/t4f/README.md](../vendor/t4f/README.md). Não copia a aplicação, infraestrutura ou documentos confidenciais.
