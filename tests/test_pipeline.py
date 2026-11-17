"""Testes com arquivos sintéticos temporários, sem conclusões analíticas."""

import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from src.analise import diagnosticar
from src.carregar_dados import ler_csv
from src.pipeline import main


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporario.cleanup)
        self.caminho = Path(self.temporario.name) / "teste.csv"

    def gravar(self, conteudo: str) -> None:
        self.caminho.write_text(conteudo, encoding="utf-8-sig")

    def test_conta_ausencias_e_preserva_original(self) -> None:
        self.gravar('cidade;valor\n"São Paulo";12\nSantos; \n;NA\n')
        original = self.caminho.read_bytes()
        resultado = diagnosticar(ler_csv(self.caminho))
        self.assertEqual(resultado["linhas"], 3)
        self.assertEqual(resultado["ausencias"], {"cidade": 1, "valor": 1})
        self.assertEqual(self.caminho.read_bytes(), original)

    def test_rejeita_estruturas_invalidas(self) -> None:
        casos = ("", "a;a\n1;2\n", "a;\n1;2\n", " a;b\n1;2\n",
                 "a;b\n1\n", "a;b\n1;2;3\n", "a;b\n", "a;b\n\n")
        for conteudo in casos:
            with self.subTest(conteudo=conteudo):
                self.gravar(conteudo)
                with self.assertRaises(ValueError):
                    diagnosticar(ler_csv(self.caminho))

    def test_aspas_e_multiplas_linhas(self) -> None:
        self.gravar('nome;valor\n"linha\nseguinte";"a;b"\n')
        self.assertEqual(diagnosticar(ler_csv(self.caminho))["linhas"], 1)

    def test_rejeita_aspas_malformadas(self) -> None:
        self.gravar('a;b\n"sem fechamento;1\n')
        with self.assertRaises(csv.Error):
            diagnosticar(ler_csv(self.caminho))

    def test_cli_retorna_json(self) -> None:
        self.gravar("a,b\n1,2\n")
        saida = io.StringIO()
        with redirect_stdout(saida):
            status = main([str(self.caminho), "--delimiter", ","])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(saida.getvalue())["linhas"], 1)

    def test_cli_trata_erros_sem_json_parcial(self) -> None:
        self.gravar("a;b\n1;2\n3\n")
        casos = ([str(self.caminho)], [str(self.caminho), "--encoding", "inexistente"],
                 [str(self.caminho), "--delimiter", "||"], [str(self.caminho) + ".ausente"])
        for argumentos in casos:
            with self.subTest(argumentos=argumentos):
                saida, erros = io.StringIO(), io.StringIO()
                with redirect_stdout(saida), redirect_stderr(erros):
                    self.assertEqual(main(argumentos), 2)
                self.assertEqual(saida.getvalue(), "")
                self.assertIn("Falha no diagnóstico", erros.getvalue())

    def test_encoding_invalido(self) -> None:
        self.caminho.write_bytes(b"a;b\n\xff;2\n")
        with self.assertRaises(UnicodeError):
            diagnosticar(ler_csv(self.caminho))


if __name__ == "__main__":
    unittest.main()
