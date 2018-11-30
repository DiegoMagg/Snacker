from re import findall
import pandas


def executa_interface():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        master = tk.Tk()
        master.title('Snacker')

        def abre_arquivo():
            arquivo = ''
            while arquivo == '':
                arquivo = filedialog.askopenfilename(
                    title="Selecionar arquivo",
                    filetypes=(("Arquivo TXT", "*.txt"),))
                if arquivo == '':
                    warn = messagebox.askquestion(
                        "Aviso", "Nenhum arquivo importado, deseja tentar novamente?"
                    )
                    if warn == 'Yes':
                        continue
                    else:
                        master.destroy()
                        break
            executa_extracao(arquivo)
            messagebox.showinfo("Completo", "Sua planilha foi exportada!")
        f = tk.Frame(master, height=200, width=300)
        f.pack()
        b = tk.Button(master, text="Abrir arquivo", command=abre_arquivo)
        b.pack(side="top", fill='both', expand=True, padx=4, pady=4)
        master.mainloop()
    except ModuleNotFoundError:
        executa_extracao(input(str('Digite o nome do arquivo: ')))


def abre_arquivo_txt(arquivo, modo):
    return open(arquivo, modo, encoding="utf-8")


def executa_extracao(arquivo):
    extracoes = []
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


executa_interface()
