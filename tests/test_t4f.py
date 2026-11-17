"""Integração das fontes, reconciliação e reprodução do snapshot."""
import copy
import unittest

from src.executar import calcular, validar_resultado
from src.gerar_demo import verificar_gerador
from src.ingestao import verificar_fontes


class T4FTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.resultado = calcular()

    def test_procedencia_e_geracao_byte_a_byte(self) -> None:
        manifesto = verificar_fontes()
        self.assertEqual(verificar_gerador(), manifesto["dataset"]["sha256"])

    def test_reconciliacao_historica(self) -> None:
        validar_resultado(self.resultado)
        self.assertEqual(self.resultado["counts"]["bookings"], 164)
        self.assertEqual(self.resultado["historical"]["travelers"], 188)
        self.assertEqual(self.resultado["satisfaction"]["n"], 72)

    def test_detecta_resultado_parcial_inconsistente(self) -> None:
        dados = copy.deepcopy(self.resultado)
        dados["historical"]["monthly"][0]["travelers"] += 1
        with self.assertRaisesRegex(ValueError, "reconciliam"):
            validar_resultado(dados)


if __name__ == "__main__":
    unittest.main()
