#!/usr/bin/env python3

from re import findall
import pandas
import sys
from PIL import ImageTk, Image


def executa_interface():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        master = tk.Tk()
        master.title('Snacker')
        logo = ImageTk.PhotoImage(Image.open('cairo92.png'))
        cairo = tk.Label(master, image=logo)
        cairo.pack(side="top", fill="both", expand="no")

        def abre_arquivo(mes):
            arquivo = ''
            while arquivo == '':
                arquivo = filedialog.askopenfilename(
                    title="Selecionar arquivo",
                    filetypes=(("Arquivo TXT", "*.txt"),))
                if not arquivo:
                    warn = messagebox.askquestion(
                        "Aviso", "Nenhum arquivo importado, deseja tentar novamente?"
                    )
                    if warn == 'yes':
                        arquivo = ''
                        continue
                    else:
                        master.destroy()
                        sys.exit()
            executa_extracao(arquivo)
            messagebox.showinfo("Completo", "Sua planilha foi exportada!")
        f = tk.Frame(master, height=50, width=300)
        f.pack()
        choices = {
            'Janeiro': '01',
            'Março': '02',
            'Fevereiro': '03',
            'Abril': '04',
            'Maio': '05',
            'Junho': '06',
            'Julho': '07',
            'Agosto': '08',
            'Setembro': '09',
            'Outubro': '10',
            'Novembro': '11',
            'Dezembro': '12',
        }
        mes = tk.StringVar(master)
        mes.set(next(iter(choices)))
        seleciona_mes = tk.OptionMenu(
            master,
            mes,
            'Janeiro',
            'Março',
            'Fevereiro',
            'Abril',
            'Maio',
            'Junho',
            'Julho',
            'Agosto',
            'Setembro',
            'Outubro',
            'Novembro',
            'Dezembro',
        )
        seleciona_mes.pack()
        b = tk.Button(master, text="Abrir arquivo", command=lambda: abre_arquivo(choices[mes.get()]))
        b.pack(side="top", fill='both', expand=False, padx=4, pady=4)
        master.mainloop()
    except ModuleNotFoundError:
        executa_extracao(input(str('Digite o nome do arquivo: ')))


def abre_arquivo_txt(arquivo, modo):
    try:
        arquivo = open(arquivo, modo, encoding="utf-8")
    except FileNotFoundError:
        print('Bye')
    return arquivo


def executa_extracao(arquivo, test=False):
    extracoes = []
    if arquivo:
        arquivo = abre_arquivo_txt(arquivo, 'r')
        linhas = arquivo.readlines()
        arquivo.close()
        for linha in linhas:
            encontra_dados = {
                    'Data': extrai_data(linha),
                    'Nome': extrai_nome(linha),
                    'Valor': extrai_valor(linha),
                    'Quantidade': extrai_quantidade(linha),
            }
            if encontra_dados['Nome'] and encontra_dados['Valor']:
                extracoes.append(tuple(encontra_dados.values()))
        grava_dados_em_csv(extracoes)
    else:
        sys.exit()
    return encontra_dados


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
    PEQUENO = 'R$6.00'
    GRANDE = 'R$8.00'
    tamanho_dict = {
        'peq': PEQUENO,
        'gra': GRANDE,
    }
    encontra_tamanho = findall(r"\((...)", linha.lower().replace(' ', ''))
    for i in encontra_tamanho:
        if i == 'peq' or i == 'gra':
            return tamanho_dict.get(i, 'erro')


def extrai_quantidade(linha):
    try:
        return findall(r"\((\d+)\)", linha)[0]
    except IndexError:
        pass


def grava_dados_em_csv(extracoes):
    for i in extracoes:
        data = pandas.DataFrame(data=extracoes, columns=['Data', 'Nome', 'Valor', 'Quantidade'])
    data.to_csv('almoco.csv', mode='a', index=False, header=True)


if __name__ == '__main__':
    executa_interface()
