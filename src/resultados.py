"""Uma única narrativa calculada para documentação, notebook e relatório."""
import json
from typing import Any

from src.config import PROCESSADOS, RAIZ


def carregar_resultados() -> dict[str, Any]:
    return json.loads((PROCESSADOS / "analise-t4f.json").read_text(encoding="utf-8"))


def formatar(valor: float, casas: int = 2) -> str:
    return f"{valor:,.{casas}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def insights(dados: dict[str, Any]) -> list[str]:
    historico, plano, modelo = dados["historical"], dados["planning"], dados["forecast"]
    selecionado = next(linha for linha in modelo["metrics"] if linha["modelId"] == modelo["selectedId"])
    return [dados["seasonality"]["conclusion"], dados["cancellations"]["conclusion"],
            dados["satisfaction"]["conclusion"],
            f"Planejamento de 07/11 a 31/12/2026: ocupação de {formatar(plano['occupancy'])}% "
            f"({plano['committed']}/{plano['capacity']} vagas-noite), com déficit de {plano['shortage']} "
            "vagas-noite em slots específicos. Negociar por saída/data/etapa/categoria; folga em outro slot não cobre a falta.",
            f"No histórico, receita contratada de R$ {formatar(historico['totalRevenue'])}, "
            f"custos de R$ {formatar(historico['cost'])} e contribuição de R$ {formatar(historico['contribution'])}. "
            "Não é lucro líquido: tributos, estornos e conciliação contábil não foram modelados.",
            f"{modelo['selected']} selecionado antes do teste final. MAE no holdout: "
            f"{formatar(selecionado['mae'], 4)} viajantes/mês; RMSE {formatar(selecionado['rmse'], 4)}. "
            "A média ponderada teve menor MAE final; não se escolheu novamente o modelo após observar o teste."]


def executar() -> None:
    dados = carregar_resultados()
    texto = "# Resultados T4F calculados\n\nDados sintéticos, seed 42; não representam desempenho real da Tour4Friends.\n\n"
    texto += "Histórico: janeiro/2024 a outubro/2026. Planejamento: 07/11 a 31/12/2026. Referência da base: 07/11/2026.\n\n"
    texto += "\n\n".join(f"{indice}. {item}" for indice, item in enumerate(insights(dados), 1))
    texto += "\n\n## Rastreabilidade\n\nSnapshot SHA-256: `" + dados["datasetSha256"] + "`. "
    texto += "Fontes e núcleo original em [fontes.json](fontes.json); contratos em [fontes-e-dicionario.md](fontes-e-dicionario.md). "
    texto += "As conclusões são geradas por `python -m src.resultados`; tabelas em `data/processed/`.\n"
    (RAIZ / "docs/resultados.md").write_text(texto, encoding="utf-8")


if __name__ == "__main__":
    executar()
