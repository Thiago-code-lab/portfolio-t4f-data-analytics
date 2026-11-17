"""Prepara cópias públicas dos anexos explicitamente fornecidos pelo autor."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from zipfile import ZipFile

import fitz

RAIZ = Path(__file__).resolve().parents[1]


def publicar_pdf(origem: Path) -> dict[str, object]:
    destino = RAIZ / "docs/referencias/projeto-big-data-t4f-publico.pdf"
    destino.parent.mkdir(parents=True, exist_ok=True)
    removidos = 0
    with fitz.open(origem) as documento:
        for pagina in documento:
            for palavra in pagina.get_text("words"):
                if re.fullmatch(r"\d{13}", palavra[4]):
                    pagina.add_redact_annot(fitz.Rect(palavra[:4]), fill=(1, 1, 1))
                    removidos += 1
            pagina.apply_redactions(images=0)
        documento.set_metadata({"title": "Análise de dados aplicada ao Caminho de Santiago - documentação acadêmica",
                                "author": "Grupo T4F Performance - Fatec Ipiranga"})
        documento.save(destino, garbage=4, deflate=True)
    with fitz.open(destino) as copia:
        if re.search(r"\b\d{13}\b", "\n".join(p.get_text() for p in copia)):
            raise ValueError("Identificador acadêmico permaneceu no documento público.")
        paginas = len(copia)
    return {"arquivo": destino.relative_to(RAIZ).as_posix(), "paginas": paginas,
            "identificadores_ocultados": removidos, "sha256": hashlib.sha256(destino.read_bytes()).hexdigest(),
            "tratamento": "Somente matrículas ocultadas; conteúdo acadêmico e figuras preservados. Não é especificação do software executado."}


def publicar_zip(origem: Path) -> dict[str, object]:
    destino = RAIZ / "anexos/bases_de_dados_T4F.zip"
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(origem, destino)
    pasta = RAIZ / "data/suplementar"
    pasta.mkdir(parents=True, exist_ok=True)
    registros = []
    with ZipFile(destino) as pacote:
        if len(pacote.infolist()) > 30 or sum(x.file_size for x in pacote.infolist()) > 10_000_000:
            raise ValueError("Pacote fora dos limites previstos.")
        for membro in pacote.infolist():
            nome = membro.filename
            if Path(nome).name != nome or membro.is_dir():
                raise ValueError("Caminho não permitido no pacote.")
            conteudo = pacote.read(nome)
            registros.append({"arquivo": nome, "bytes": len(conteudo), "sha256": hashlib.sha256(conteudo).hexdigest()})
            if nome.endswith(".csv"):
                (pasta / nome).write_bytes(conteudo)
    return {"arquivo": destino.relative_to(RAIZ).as_posix(), "sha256": hashlib.sha256(destino.read_bytes()).hexdigest(),
            "conteudo": registros, "natureza": "Pacote fornecido pelo autor: simulação seed 2026 e tabelas externas de referência sem certificação primária."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--zip", type=Path, required=True)
    opcoes = parser.parse_args()
    dados = {"recebido_em": "2026-11-17", "pdf": publicar_pdf(opcoes.pdf), "zip": publicar_zip(opcoes.zip)}
    (RAIZ / "docs/anexos-manifesto.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
