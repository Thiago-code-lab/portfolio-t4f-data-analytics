# Bases acadêmicas complementares

Origem: ZIP fornecido pelo autor em 17/11/2026. [Arquivo original](../anexos/bases_de_dados_T4F.zip) preservado byte a byte; [manifesto](anexos-manifesto.json) com hashes e tamanhos de todos os 12 membros. Não é o snapshot da demonstração principal e não contém o histórico privado real da empresa.

O pacote contém nove CSVs, um XLSX de dez abas, LEIA-ME e gerador Python. A planilha é uma cópia tabular, sem fórmulas, macros ou vínculos externos; metadados identificam openpyxl. Foi inspecionada como entrada, sem modificações. Os nove CSVs foram extraídos com nomes originais para data/suplementar e verificados por SHA-256. O gerador anexado foi lido, mas não executado automaticamente.

| Base | Linhas | Natureza e limite |
| --- | ---: | --- |
| Clientes | 422 | Perfis fictícios; IDs e faixas, sem nomes/contatos reais |
| Reservas | 469 | Simulação seed 2026; 402 realizadas, 29 confirmadas e 38 canceladas |
| Feedbacks | 300 | NPS 72 imposto; 293 respostas até 16/11/2026, sete futuras |
| Ocupação | 4.662 | Slots sintéticos de etapa/data/categoria, independentes de reservas |
| Financeiro mensal | 7 | BRL ilustrativo; junho é citado na apresentação, sem comprovação contábil |
| Clima | 12 | Tabela fornecida, atribuída a fonte secundária; sem homologação meteorológica |
| Feriados | 76 | Calculados por calendário; não tratados como calendário legal homologado |
| Brasileiros por caminho | 7 | Duas fontes concorrentes; não somar versões ou duplicar totais |
| Série mensal de peregrinos | 12 | Transcrição secundária; não certificada como série oficial nesta entrega |

## Contratos e cortes

Reservas usam EUR e Econômico/Standard/Superior; a demo principal usa BRL e Premium/Conforto/Alternativa. Não existe mapeamento automático entre essas categorias. Financeiro e ocupação não possuem chaves conciliáveis com reservas: não comparar somas como se viessem do mesmo livro transacional.

O pipeline valida hashes, PK/FK entre clientes/reservas/feedbacks, nulos nas chaves, datas, antecedência, domínio de categorias/status, valores positivos, slots únicos, taxa e déficit por slot e contribuição = receita − custo. Erros interrompem a análise, sem corrigir a fonte silenciosamente.

O gerador classifica “realizada” pelo início da viagem; isso não comprova conclusão. No corte de respostas em 16/11/2026, NPS = 72,70 pontos sobre 293 respostas; sete futuras não entram nesse indicador. NPS total = 72 em 300 é uma premissa imposta no gerador, não descoberta da qualidade real.

Portomarín, 14/11/2026, Superior: capacidade 2, comprometimento 3, ocupação 150%, falta 1 vaga-noite. A ocupação agregada da base é 59,05%, com três vagas-noite de falta somadas após calcular por slot. Folga em outra data não compensa a falta.

## Fontes externas

O LEIA-ME atribui a série de chegadas a um site secundário que cita a Oficina del Peregrino e registra divergências entre duas versões dos números brasileiros. [Fonte primária indicada](https://oficinadelperegrino.com/estadisticas/). Este portfólio não certifica as transcrições; seu uso é documental, não alimenta o treino principal. O prefixo original real_ foi preservado como nome recebido, não como selo de validação.

Reprodução: `python -m src.suplementar`. Saída: data/processed/analise-suplementar.json. O notebook apresenta contagens, NPS com corte e exemplo de capacidade, separados da demonstração principal.
