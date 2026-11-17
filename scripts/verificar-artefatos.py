"""Verificações semânticas das entregas; revisão visual continua obrigatória."""
from pathlib import Path
import json
import re
import sys

import fitz
from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from src.ingestao import verificar_fontes
from src.resultados import carregar_resultados, formatar


def verificar_notebook() -> int:
    notebook = json.loads((RAIZ / "notebooks/analise_exploratoria.ipynb").read_text(encoding="utf-8"))
    codigos = [celula for celula in notebook["cells"] if celula["cell_type"] == "code"]
    if not all(celula.get("execution_count") for celula in codigos):
        raise ValueError("Notebook contém código não executado.")
    if any(saida["output_type"] == "error" for celula in codigos for saida in celula.get("outputs", [])):
        raise ValueError("Notebook contém saída de erro.")
    return len(codigos)


def verificar_pdf() -> int:
    dados = carregar_resultados()
    with fitz.open(RAIZ / "output/pdf/portfolio-t4f-performance.pdf") as documento:
        if len(documento) != 8:
            raise ValueError("Paginação inesperada do relatório.")
        texto = "\n".join(pagina.get_text() for pagina in documento)
        for esperado in (dados["datasetSha256"], "T4F Performance", formatar(dados["historical"]["contribution"]), "500"):
            if esperado not in texto:
                raise ValueError(f"Evidência ausente no PDF: {esperado}")
        for pagina in documento:
            if any(palavra[0] < 20 or palavra[2] > pagina.rect.width - 20 for palavra in pagina.get_text("words")):
                raise ValueError("Texto fora das margens do PDF.")
        return len(documento)


def verificar_links() -> int:
    quantidade = 0
    for arquivo in RAIZ.rglob("*.md"):
        if any(parte in {".venv", "node_modules", ".git", "tmp"} for parte in arquivo.relative_to(RAIZ).parts):
            continue
        for destino in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', arquivo.read_text(encoding="utf-8-sig")):
            if "://" in destino or destino.startswith("#"):
                continue
            caminho = destino.split("#", 1)[0]
            if caminho and not (arquivo.parent / caminho).exists():
                raise ValueError(f"Link local ausente: {arquivo.name} -> {destino}")
            quantidade += 1
    return quantidade


def main() -> None:
    verificar_fontes()
    graficos = list((RAIZ / "visualizacoes").glob("*.png"))
    if len(graficos) != 6:
        raise ValueError("Esperados seis gráficos.")
    for grafico in graficos:
        with Image.open(grafico) as imagem:
            if imagem.width < 1200 or imagem.height < 600:
                raise ValueError(f"Resolução insuficiente: {grafico.name}")
    resultado = {"fontes_integras": True, "graficos": len(graficos),
                 "celulas_executadas": verificar_notebook(), "paginas_pdf": verificar_pdf(),
                 "links_locais": verificar_links(), "revisao_visual": "registrada em docs/verificacao.md"}
    print(json.dumps(resultado, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
