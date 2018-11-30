# Snacker - Python

Este projeto visa facilitar a contagem de pedidos de almoço realizados via whatsapp no coworking Cairo 92.
O Snacker usa o export em txt de uma conversa no app, encontra o padrão predefinido e exporta os dados para um arquivo csv (comma separated values).
Padrão adotado: \*Nome:\* (tamanho) (quantidade): Menu

### Como Usar
Instale o pipenv. 
[Clique aqui](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/) caso não tenha o pip3 instalado.
```sh
$ sudo apt update
$ pip install pipenv
```
Baixe e extraia a aplicação.
https://github.com/DiegoMagg/Snacker/releases

Dentro do conteúdo extraído execute:
```sh
$ pipenv install --three
$ pipenv run python almoco.py
```

Outros comandos:
```sh
$ pipenv run python test.py
```
