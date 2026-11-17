"""Contratos e segregação da base acadêmica complementar."""
import copy
import unittest

from src.suplementar import analisar, carregar, validar


class SuplementarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tabelas = carregar()

    def test_cenario_fornecido_e_natureza_distinta(self) -> None:
        dados = analisar(self.tabelas)
        self.assertEqual(dados["contagens"]["sintetico_reservas"], 469)
        self.assertEqual(dados["nps_total"], 72)
        self.assertEqual(dados["portomarin"]["taxa_pct"], 150)
        self.assertGreater(dados["respostas_futuras"], 0)

    def test_rejeita_relacao_inexistente(self) -> None:
        tabelas = copy.deepcopy(self.tabelas)
        tabelas["sintetico_reservas"].loc[0, "id_cliente"] = -1
        with self.assertRaisesRegex(ValueError, "Cliente"):
            validar(tabelas)

    def test_rejeita_slot_duplicado(self) -> None:
        import pandas as pd
        tabelas = copy.deepcopy(self.tabelas)
        original = tabelas["sintetico_ocupacao_hospedagens"]
        tabelas["sintetico_ocupacao_hospedagens"] = pd.concat([original, original.iloc[:1]])
        with self.assertRaisesRegex(ValueError, "Slot"):
            validar(tabelas)


if __name__ == "__main__":
    unittest.main()
