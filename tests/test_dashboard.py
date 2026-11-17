"""Fluxos reais do leitor e ausência de dados sem alterar arquivos do projeto."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from src.config import RAIZ


class DashboardTests(unittest.TestCase):
    def test_filtro_por_roteiro_mantem_planejamento_global(self) -> None:
        app = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=20).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "188")
        app.sidebar.selectbox[0].set_value("santiago").run()
        self.assertFalse(app.exception)
        self.assertNotEqual(app.metric[0].value, "188")
        self.assertIn("4 vagas-noite", app.warning[0].value)

    def test_dados_ausentes_exibem_erro_e_reproducao(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            with patch("src.config.PROCESSADOS", Path(pasta)):
                app = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=20).run()
        self.assertFalse(app.exception)
        self.assertIn("Análise indisponível", app.error[0].value)
        self.assertIn("src.executar", app.code[0].value)


if __name__ == "__main__":
    unittest.main()
