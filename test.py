import unittest
from almoco import (
    abre_arquivo_txt,
    coleta_pedido,
    extrai_data,
    extrai_nome,
    extrai_quantidade,
    extrai_valor,
)


class ArquivoTxt(unittest.TestCase):
    dados = None

    def setUp(self):
        try:
            arquivo_txt = open('almoco_teste.txt', 'r')
            self.dados = arquivo_txt.readline()
            arquivo_txt.close()
        except FileNotFoundError:
            with open('almoco_test.txt', 'w', encoding='utf-8') as txt:
                txt.write('10/9/18, 11:04 AM - Nome: *Nome:* (pequeno) (1); Menu.')
                txt.close()
            arquivo_txt = open('almoco_test.txt', 'r', encoding='utf-8')
            self.dados = arquivo_txt.readline()
            arquivo_txt.close()

    def test_dado_deve_ser_uma_string(self):
        self.assertIs(str, type(self.dados))

    def test_data_deve_ser_obtida(self):
        data = extrai_data(self.dados)
        self.assertEqual('10/9/18', data)

    def test_nome_deve_ser_obtido(self):
        nome = extrai_nome(self.dados)
        self.assertEqual('Nome', nome)

    def test_valor_do_pedido_deve_ser_extraido(self):
        valor = extrai_valor(self.dados)
        self.assertEqual('$6.00', valor)

    def test_quantidade_deve_ser_extraida(self):
        quantidade = extrai_quantidade(self.dados)
        self.assertEqual('1', quantidade)

    def test_deve_retornar_dict_com_os_dados_corretamente(self):
        pedido_completo = coleta_pedido(self.dados)
        self.assertEqual(
            {'Data': '10/9/18', 'Nome': 'Nome', 'Valor': '$6.00', 'Quantidade': '1'},
            pedido_completo
        )


if __name__ == '__main__':
    unittest.main()
