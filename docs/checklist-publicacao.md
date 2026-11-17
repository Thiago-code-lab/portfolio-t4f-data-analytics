# Checklist de publicação

Destino: [Thiago-code-lab/portfolio-t4f-data-analytics](https://github.com/Thiago-code-lab/portfolio-t4f-data-analytics), main. Data: 17/11/2026.

| Verificação | Estado | Evidência |
| --- | --- | --- |
| Backup restaurável externo | OK | Auditoria local: 274 arquivos/4.892.325 bytes idênticos, inclusive .git |
| Histórico anterior apenas local | OK | arquivo-local/pre-publicacao; raiz pública independente |
| Diretório e destino confirmados | OK | rev-parse e ls-remote; destino sem branches na preparação |
| Original somente leitura | OK | Remoto confirmado; preservacao-original.json |
| Problema → dados → pipeline → decisão | OK | README, problema.md, notebook e resultados.md |
| Metodologias e evidências | OK | metodologias.md e leitura-documentacao.md, páginas identificadas |
| ZIP original íntegro | OK | anexos-manifesto.json; 12 membros conferidos |
| Documentação acadêmica | OK | PDF público de 30 páginas, dez matrículas ocultadas |
| Base privada da empresa | NÃO SE APLICA | Não fornecida; simulações e referências secundárias |
| Categorias, moedas e cortes separados | OK | bases-suplementares.md e src.suplementar |
| Instalação limpa e reprodução | OK | verificacao.md, ambiente Python vazio e npm ci |
| Testes e TypeScript | OK | 23 testes aprovados e typecheck |
| Notebook e seis gráficos | OK | Nove células executadas; PNGs inspecionados |
| Dois PDFs e privacidade | OK | 30 páginas da referência e oito do relatório renderizadas/revisadas |
| Streamlit e tratamento de erros | OK | HTTP 200 e dois AppTest |
| Navegação visual interativa | PENDENTE | Pipe nativo e navegador iab indisponíveis; não se declara homologação |
| Fontes externas primárias | PENDENTE | Tabelas secundárias qualificadas; sem certificação oficial ou uso no treino principal |
| Segredos, caminhos e dados pessoais | PENDENTE | Conferência final do material antes do commit |
| Links, staging e histórico público | PENDENTE | Revisão integral antes do commit |
| Push e SHA remoto | PENDENTE | Somente HEAD:main; não enviar branches/tags locais |
| Navegação e arquivos públicos | PENDENTE | Conferência remota após push |
| Actions / Pages | NÃO SE APLICA | Nenhum workflow ou implantação incluído |
| LinkedIn | NÃO SE APLICA | Texto preparado, sem envio da postagem |

Limitações de navegador e das referências secundárias são explícitas. A simulação principal é controlada e reproduzível sem essas fontes externas.
