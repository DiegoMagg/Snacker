from re import findall
import csv


def abre_arquivo_txt(arquivo, modo):
    return open(arquivo, modo, encoding="utf-8")


def separa_linha_para_coleta(arquivo):
    arquivo = abre_arquivo_txt(arquivo, 'r')
    linhas = arquivo.readlines()
    for linha in linhas:
        coleta_pedido(linha)


def coleta_pedido(linha):
    extracoes = {
        'Data': extrai_data(linha),
        'Nome': extrai_nome(linha),
        'Valor': extrai_valor(linha),
        'Quantidade': extrai_quantidade(linha),
    }
    grava_dados_em_csv(extracoes)
    return extracoes


def extrai_data(linha):
    try:
        data = findall(r"\d+\/\d+\/\d+", linha)[0]
        return data
    except IndexError:
        pass


def extrai_nome(linha):
    try:
        nome = findall(r"\*(\w+)", linha)[0]
        return nome
    except IndexError:
        pass


def extrai_valor(linha):
    try:
        if findall(r"\((\w{6,7})\)", linha)[0].capitalize() == 'Pequeno':
            return '$6.00'
        else:
            return '$8.00'
    except IndexError:
        pass


def extrai_quantidade(linha):
    try:
        return findall(r"\((\d+)\)", linha)[0]
    except IndexError:
        pass


def grava_dados_em_csv(dado):
    carrega_csv = open('almoco.csv', 'r')
    lista_csv = list(csv.reader(carrega_csv))
    carrega_csv.close()
    with open('almoco.csv', 'a', newline='') as csvfile:
        colunas = ['Data', 'Nome', 'Valor', 'Quantidade']
        gravador = csv.DictWriter(csvfile, fieldnames=colunas)
        if dado['Nome'] and dado['Valor']:
            if lista_csv == [] or lista_csv[0] != colunas:
                gravador.writeheader()
            gravador.writerow(dado)
        else:
            pass


separa_linha_para_coleta('almoco.txt')
