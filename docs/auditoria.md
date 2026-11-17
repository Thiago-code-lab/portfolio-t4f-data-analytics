# Auditoria de preparação para publicação

Em 17/11/2026 foram conferidos diretório Git, arquivos rastreados/não rastreados e destino remoto. O destino informado estava sem branches. Foi criado backup externo restaurável com `.git`, arquivos de trabalho e saídas, excluindo ambientes e caches. O manifesto local confirmou 274 arquivos e 4.892.325 bytes idênticos.

O histórico de trabalho foi mantido exclusivamente em backup e na branch local `arquivo-local/pre-publicacao`. A branch pública `main` foi preparada com uma raiz independente no mesmo repositório. Somente `HEAD:main` é enviado; a branch de arquivo e quaisquer tags locais não são publicadas.

O projeto integrador foi descoberto e confirmado pelo remoto original, consultado apenas em leitura. Seu status e 192 hashes de arquivos foram registrados para comparação final. A cópia pública contém somente o núcleo analítico selecionado, não a aplicação completa.

Documentação e ZIP fornecidos foram inspecionados. O ZIP não contém a base privada da empresa; a cópia pública do PDF remove dez matrículas. O original acadêmico e as instruções de operação permanecem no backup local. Evidências finais no [checklist](checklist-publicacao.md), [verificação](verificacao.md) e [manifesto dos anexos](anexos-manifesto.json).
