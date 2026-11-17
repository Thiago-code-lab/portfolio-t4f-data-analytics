# Verificação para publicação — 17/11/2026

Windows, Python 3.12.10 e Node.js 24.14.1. Criado ambiente Python vazio fora do repositório e instalado requirements-dev.txt, que inclui requirements.txt. npm ci instalou a árvore fixada no lock. Nenhuma instalação, geração ou teste foi executado no projeto original.

| Verificação | Resultado executado |
| --- | --- |
| Instalação limpa | requirements-dev.txt e npm ci aprovados |
| TypeScript | npm run typecheck aprovado |
| Testes Node | Oito aprovados, zero falhas |
| Testes Python | 15 aprovados: sete CSV, três T4F, três complementares e dois AppTest |
| Pipeline principal | 164 reservas, 144 históricas e 188 participações; receitas/contagens reconciliadas |
| Gerador principal | Seed 42 reproduzido byte a byte no teste de integração |
| Base complementar | Nove CSVs contra o ZIP; PK/FK, datas, taxas, slots e contribuição validados |
| Corte dos feedbacks | 300 totais, sete futuras; 293 até 16/11/2026, NPS 72,70 pontos |
| Notebook | Nove células executadas no ambiente limpo, sem erro ou estado oculto |
| Gráficos | Seis PNGs com revisão visual, fontes, unidades e amostras |
| Relatório | Oito páginas A4 renderizadas/inspecionadas; texto/margens conferidos |
| Documento acadêmico | 30 páginas inspecionadas; dez matrículas removidas da cópia pública |
| ZIP e XLSX | ZIP idêntico ao recebido; 12 membros; XLSX com dez abas, sem fórmulas/macros/vínculos externos |
| Streamlit | Servidor real em loopback; health HTTP 200, conteúdo ok |
| Fluxos Streamlit | AppTest: filtro, indicadores, planejamento global e arquivo ausente aprovados |
| Browser interativo | Não executado: pipe nativo e navegador iab indisponíveis; sem homologação visual interativa |

**23 testes aprovados**, oito Node e 15 Python. Avisos ScriptRunContext do AppTest não causaram falhas. O serviço de validação é encerrado após a conferência. Não foi criado site no Pages.

## Reprodução

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
npm.cmd ci
npm.cmd run typecheck
npm.cmd test
.\.venv\Scripts\python.exe -m src.executar
.\.venv\Scripts\python.exe -m src.suplementar
.\.venv\Scripts\python.exe -m src.visualizacoes
.\.venv\Scripts\python.exe -m src.resultados
.\.venv\Scripts\python.exe -m src.notebook
.\.venv\Scripts\python.exe -m src.relatorio
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/verificar-artefatos.py
```

PDFs renderizados com PyMuPDF disponível; Poppler não estava no PATH. Páginas individuais e folhas de contato são temporárias. A verificação semântica examina notebook, fontes, gráficos, números, paginação e links; não substitui a revisão visual.

Dados da demo e do ZIP permanecem separados. Fontes externas do pacote não foram certificadas como estatísticas oficiais ou calendário legal. Modelos, quatro sprints, Power BI e automação semanal descritos no documento não são declarados executados sem evidência.

O histórico público tem raiz própria do T4F; o arquivo local não é enviado. Integridade do original em preservacao-original.json; publicação e inspeção remota no [checklist](checklist-publicacao.md).
