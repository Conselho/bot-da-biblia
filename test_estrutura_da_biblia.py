import unittest
import estrutura_da_biblia


class TestEstrutura(unittest.TestCase):

    def test_abreviatura_from_str(self):
        for key in estrutura_da_biblia.biblia:
            self.assertTrue(estrutura_da_biblia.abreviatura_from_str(key))
            for nome_alternativo in estrutura_da_biblia.biblia[key]["nomes_alternativos"]:
                self.assertTrue(estrutura_da_biblia.abreviatura_from_str(nome_alternativo))

    def test_capitulo_existe(self):
        """
        Verificar se o algoritmo de verificação de capítulos funciona corretamente para cada nome possível e cada
        capítulo possível.
        """
        verificar_capitulo: () = lambda k, n: estrutura_da_biblia.capitulo_existe(k, n)
        loop_capitulos_verificar_capitulos: () = lambda k, n: self.loop_capitulos(k, n, verificar_capitulo)
        TestEstrutura.loop_keys_nomes_alternativos(loop_capitulos_verificar_capitulos)

    def test_versiculo_existe(self):
        """
        Testar a função de verificação de versículos
        """
        versiculo_existe: () = lambda k, n, v: estrutura_da_biblia.versiculo_existe(k, n, v)
        for key in estrutura_da_biblia.biblia:
            self.loop_versiculos(key, key, versiculo_existe)
            for nome_alternativo in estrutura_da_biblia.biblia[key]["nomes_alternativos"]:
                self.loop_versiculos(key, nome_alternativo, versiculo_existe)

    def test_get_referencia_from_str(self):
        """
        Testar se o algoritmo de leitura de referências funciona
        """
        # <l> <c>
        #   situação válida

        # TestEstrutura.loop_keys_nomes_alternativos()  #
        res = estrutura_da_biblia.get_referencia_from_str("Ef 6")
        exp = estrutura_da_biblia.ReferenciaBiblica("Ef", 6, set())
        self.assertEqual(res, exp)
        #   livro inválido
        res = estrutura_da_biblia.get_referencia_from_str("Oflo ghe 1")
        self.assertFalse(res)
        #   capítulo inválido 1
        res = estrutura_da_biblia.get_referencia_from_str("Filipenses 5")
        self.assertFalse(res)
        #   capítulo inválido 2
        res = estrutura_da_biblia.get_referencia_from_str("Segunda Carta de S. Paulo aos Tessalonicences 0")
        self.assertFalse(res)
        # <l> <c>, <v>
        #   situação válida
        res = estrutura_da_biblia.get_referencia_from_str("1 Tessalonicenses 5, 10")
        exp = estrutura_da_biblia.ReferenciaBiblica("1Ts", 5, {10})
        self.assertEqual(res, exp)
        #   livro inválido
        res = estrutura_da_biblia.get_referencia_from_str("1 Falso 1, 3")
        self.assertFalse(res)
        #   capítulo inválido 1
        res = estrutura_da_biblia.get_referencia_from_str("Romanos 20, 1")
        self.assertFalse(res)
        #   capítulo inválido 2
        res = estrutura_da_biblia.get_referencia_from_str("Romanos -3, 3")
        self.assertFalse(res)
        # <l> <c>, <v_inicial>-<v_final>
        #   situação válida
        res = estrutura_da_biblia.get_referencia_from_str("carta de s. paulo aos colossenses 4, 12-18")
        self.assertEqual(estrutura_da_biblia.ReferenciaBiblica("Cl", 4, {12, 13, 14, 15, 16, 17, 18}), res)
        #   livro inválido
        res = estrutura_da_biblia.get_referencia_from_str("Falso 3, 1-2")
        self.assertFalse(res)
        # capítulo inválido 1
        res = estrutura_da_biblia.get_referencia_from_str("1 Coríntios 19, 8-10")
        self.assertFalse(res)
        # capítulo inválido 2
        res = estrutura_da_biblia.get_referencia_from_str("1Co 0, 1-2")
        self.assertFalse(res)
        # versículos inválidos
        res = estrutura_da_biblia.get_referencia_from_str("1Coríntios 10, 30-35")
        self.assertFalse(res)
        # <l> <c>, <v>.[...].<v_inicial>-<v_final>.[...]
        # situação válida
        res = estrutura_da_biblia.get_referencia_from_str("1Co 7, 3.6.30-35.39-40.10")
        self.assertEqual(estrutura_da_biblia.ReferenciaBiblica("1Co", 7, {3, 6, 30, 31, 32, 33, 34, 35, 39, 40, 10}),
                         res)
        # versículo inválido 1
        res = estrutura_da_biblia.get_referencia_from_str("Tito 2, 18")
        self.assertEqual(estrutura_da_biblia.ReferenciaBiblica("Tt", 2, set()), res)
        # versículo inválido 2
        res = estrutura_da_biblia.get_referencia_from_str("Tito 2, 4-10.15.18")
        self.assertEqual(estrutura_da_biblia.ReferenciaBiblica("Tt", 2, {4, 5, 6, 7, 8, 9, 10, 15}), res)
        # intervalo de versículos inválido
        res = estrutura_da_biblia.get_referencia_from_str("Hebreus 13, 15.20-23.24-26")
        self.assertEqual(res, estrutura_da_biblia.ReferenciaBiblica("Hb", 13, {15, 20, 21, 22, 23, 24, 25}))

        # <l> <c>: <v>
        #   situação válida
        res = estrutura_da_biblia.get_referencia_from_str("1 Tessalonicenses 5: 10")
        exp = estrutura_da_biblia.ReferenciaBiblica("1Ts", 5, {10})
        self.assertEqual(res, exp)
        #   livro inválido
        res = estrutura_da_biblia.get_referencia_from_str("1 Falso 1: 3")
        self.assertFalse(res)
        #   capítulo inválido 1
        res = estrutura_da_biblia.get_referencia_from_str("Romanos 20: 1")
        self.assertFalse(res)
        #   capítulo inválido 2
        res = estrutura_da_biblia.get_referencia_from_str("Romanos -3: 3")
        self.assertFalse(res)
        # <l> <c>: <v_inicial>-<v_final>
        #   situação válida
        res = estrutura_da_biblia.get_referencia_from_str("carta de s. paulo aos colossenses 4: 12-18")
        self.assertEqual(estrutura_da_biblia.ReferenciaBiblica("Cl", 4, {12, 13, 14, 15, 16, 17, 18}), res)
        #   livro inválido
        res = estrutura_da_biblia.get_referencia_from_str("Falso 3: 1-2")
        self.assertFalse(res)
        # capítulo inválido 1
        res = estrutura_da_biblia.get_referencia_from_str("1 Coríntios 19: 8-10")
        self.assertFalse(res)
        # capítulo inválido 2
        res = estrutura_da_biblia.get_referencia_from_str("1Co 0: 1-2")
        self.assertFalse(res)
        # versículos inválidos
        res = estrutura_da_biblia.get_referencia_from_str("1Coríntios 10: 30-35")
        self.assertFalse(res)
        # <l> <c>: <v>.[...].<v_inicial>-<v_final>.[...]
        # situação válida
        res = estrutura_da_biblia.get_referencia_from_str("1Co 7: 3.6.30-35.39-40.10")
        self.assertEqual(estrutura_da_biblia.ReferenciaBiblica("1Co", 7, {3, 6, 30, 31, 32, 33, 34, 35, 39, 40, 10}),
                         res)
        # versículo inválido 1
        res = estrutura_da_biblia.get_referencia_from_str("Tito 2: 18")
        self.assertEqual(estrutura_da_biblia.ReferenciaBiblica("Tt", 2, set()), res)
        # versículo inválido 2
        res = estrutura_da_biblia.get_referencia_from_str("Tito 2: 4-10.15.18")
        self.assertEqual(estrutura_da_biblia.ReferenciaBiblica("Tt", 2, {4, 5, 6, 7, 8, 9, 10, 15}), res)
        # intervalo de versículos inválido
        res = estrutura_da_biblia.get_referencia_from_str("Hebreus 13: 15.20-23.24-26")
        self.assertEqual(res, estrutura_da_biblia.ReferenciaBiblica("Hb", 13, {15, 20, 21, 22, 23, 24, 25}))

    @staticmethod
    def loop_keys_nomes_alternativos(action):
        """
        Passar sobre todas as keys e nomes alternativos, realizando uma ação utilizando a chave e o nome.
        :param action: ação a realizar
        """
        for key in estrutura_da_biblia.biblia:
            action(key, key)
            for nome_alternativo in estrutura_da_biblia.biblia[key]["nomes_alternativos"]:
                action(key, nome_alternativo)

    def loop_capitulos(self, key: str, nome_livro: str, action):
        """
        Verifica uma ação para todos os valores válidos e não válidos para capítulos de uma dada key
        :param key: key no JSON
        :param nome_livro: nome a utilizar
        :param action: ação a verificar com a informação de capítulo e de nome a utilizar
        """
        # o valor não pode ser negativo
        for capitulo in range(-200, 1):
            self.assertFalse(action(nome_livro, capitulo))
        n_capitulos = len(estrutura_da_biblia.biblia[key]["capitulos"])
        # o valor tem de estar entre 1 e o número de capítulos
        for capitulo in range(1, n_capitulos + 1):
            self.assertTrue(action(nome_livro, capitulo))
        # o valor não pode ser maior que o número de capítulos
        for capitulo in range(n_capitulos + 1, 200):
            self.assertFalse(action(nome_livro, capitulo))

    def loop_versiculos(self, key: str, nome: str, action):
        for capitulo in range(1, len(estrutura_da_biblia.biblia[key]["capitulos"]) + 1):
            # testar números inválidos
            for versiculo in range(-200, 1):
                self.assertFalse(action(nome, capitulo, versiculo))
            # testar versículos existentes
            n_versiculos = estrutura_da_biblia.biblia[key]["capitulos"][
                capitulo - 1]  # os capítulos são contados de 1 a
            # N mas os índices são contados desde 0 por isso é preciso subtrair 1
            for versiculo in range(1, n_versiculos + 1):
                self.assertTrue(action(nome, capitulo, versiculo))
            # testar versículos inválidos (valores superiores)
            for versiculo in range(n_versiculos + 1, 200):
                self.assertFalse(action(nome, capitulo, versiculo))


if __name__ == '__main__':
    unittest.main()
