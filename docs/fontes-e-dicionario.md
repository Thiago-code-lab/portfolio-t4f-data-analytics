# Origem, dados e contratos

Fonte: [Projeto Integrador V — Dashboards-Tour4Friends](https://github.com/Thiago-code-lab/Dashboards-Tour4Friends/tree/0216dce5f67b83fbb0ba84346a7742dcb4f5ce23), commit 0216dce. Snapshot local: `data/raw/t4f-demo.json`. Manifesto SHA-256: [fontes.json](fontes.json).

Dados **sintéticos**, versão 1.0.0, seed 42. Gerador original em `vendor/t4f/scripts/generate_demo_data.py`; reprodução byte a byte via `python -m src.gerar_demo`, em pasta temporária. Não foram usados dados pessoais reais, contratos ou documentos comerciais. Referência temporal 07/11/2026; histórico 01/01/2024–31/10/2026. Moeda BRL demonstrativa; não converter tarifas EUR de outras branches para preencher esta base.

| Coleção | Quantidade | Granularidade e relação |
| --- | ---: | --- |
| customers | 116 | Pessoa fictícia; ID e rótulo sem contato |
| bookings | 164 | Reserva total; titular, participantes, lead e saída |
| leads | 258 | Primeiro contato; roteiro, canal e estágio |
| routes | 6 | Roteiro de referência, modalidade e etapas |
| departures | 52 | Saída com início/fim e capacidade física |
| partners | 12 | Hospedagem demonstrativa de um roteiro |
| allocations | 609 | Slot por saída/data/etapa/categoria |
| costs | 156 | Rubrica de custo da saída; real/estimada no cenário |
| payments | 147 | Recebimento vinculado a reserva |
| feedback | 72 | Avaliação pós-viagem de reserva confirmada |

Schema executável: `vendor/t4f/src/types/domain.ts`; regras relacionais: `vendor/t4f/src/lib/validation/dataset.ts`. IDs únicos, FKs existentes, datas ISO calendáricas, números finitos/não negativos, enums explícitos, participantes únicos na mesma saída ativa, pagamentos compatíveis e feedback posterior à viagem. O snapshot só entra na análise depois de validar tudo.

## Preparação e qualidade

A base gerada já é estruturada. Seleção, validação de tipos, chaves e relações fazem a preparação; não se inventam sujeiras removidas ou imputações. Erros são recusados, sem transformação silenciosa de dados externos. Arquivos fora do manifesto são rejeitados no fluxo padrão. Não há credenciais ou coleta operacional no portfólio.

## Indicadores e unidades

- Demanda: soma de participantes de confirmadas por mês de início da viagem. Participações diferem de clientes únicos.
- Receita contratada: soma de totalAmount das confirmadas, uma vez por reserva. Realizada gerencial: viagens concluídas até a referência. Contratada = realizada + futura.
- Recebimentos: pagamentos das reservas selecionadas; não somar à receita.
- Contribuição: receita contratada − custos. Não é lucro líquido; margem usa receita como denominador.
- Ocupação: 100 × comprometimento/capacidade dos mesmos slots. Somar datas produz vagas-noite. Déficit é soma de max(0, comprometimento − capacidade) por slot, antes de agregar.
- NPS em pontos: 100 × (promotores 9–10 − detratores 0–6)/respostas. Notas 7–8 são neutras. Denominador vazio é null.
- Cancelamento: canceladas/todas as reservas da mesma coorte de viagem. Wilson é exploratório sob independência imperfeita.
- Conversão: leads únicos por primeiro contato com reserva confirmada vinculada / leads únicos daquela coorte. Não igualar à coorte de viagens.
- Custo por categoria no original: rateio por receita, sem inventar despesas individuais.

Histórico principal usa início da viagem entre jan/2024 e out/2026. A satisfação exploratória aplica ainda data da resposta até o corte. Planejamento usa 07/11–31/12/2026; a saída de jan/2027 está na base completa e fora desse recorte.

## Limites

Série curta, seleção de respondentes e status retrospectivos. O cenário inclui outros roteiros além de Santiago. Nenhum indicador comprova desempenho real, causalidade, market share, disponibilidade comercial ou lucro. Detalhes de modelos e estado do original em [projeto-original.md](projeto-original.md).


## Fontes adicionais recebidas

O ZIP acadêmico complementar possui outro schema, moeda e referência temporal. Ver bases-suplementares.md e anexos-manifesto.json. A documentação acadêmica de 30 páginas está em referencias/projeto-big-data-t4f-publico.pdf, com matrículas ocultadas e cotejo em leitura-documentacao.md.
