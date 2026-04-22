# Manipulação de arquivos em Python

#Arquivo de texto
with open ("dados.txt", "w") as arquivo:
    arquivo.write("Python é uma linguagem poderosa\n")
    arquivo.write("Estamos aprendendo arquivos.")


with open ("dados.txt", "r") as arquivo:
    conteudo = arquivo.read()

print(conteudo)    

with open ("dados.txt", "r") as arquivo:
    for linha in arquivo:
        print(linha.strip())


with open ("relatorio.txt", "w") as arquivo:
    arquivo.write("Relatorio de vendas\n")
    arquivo.write("Total: 1500")

with open ("relatorio.txt", "a") as arquivo:
    arquivo.write("\nNovo registro adicionado.")
    
with open ("relatorio.txt", "r") as arquivo:
    for linha in arquivo:
        print(linha.strip())

#Arquivo CSV
import csv

dados = [
    ["Nome", "Idade", "Cidade"],
    ["Alice", 30, "São Paulo"],
    ["Bob", 25, "Rio de Janeiro"],
    ["Charlie", 35, "Belo Horizonte"]
]

with open ("pessoas.csv", "w", newline="") as arquivo:
    writer = csv.writer(arquivo)
    writer.writerows(dados)

#Arquivo JSON
import json

pessoa = {
    "nome": "Alice",
    "idade": 30,
    "cidade": "São Paulo"
}

with open ("pessoa.json", "w") as arquivo:
    json.dump(pessoa, arquivo)


import urllib.request
url = "https://api.agify.io/?name=Eduardo"
with urllib.request.urlopen(url) as resposta:
    conteudo = resposta.read().decode("utf-8")
    print(conteudo)

url = "https://api.agify.io/?name=Cybelle"
with urllib.request.urlopen(url) as resposta:
    conteudo = json.loads(resposta.read().decode("utf-8"))
    print("Nome", conteudo["name"])
    print("Idade", conteudo["age"])
    print("Numero de registros:", conteudo["count"])

import sqlite3
conexao = sqlite3.connect("pessoas.db")

cursor = conexao.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        idade INTEGER,
        cidade TEXT
    );
    """
)

conexao.commit()

cursor.execute(
    "INSERT INTO pessoas (nome, idade, cidade) VALUES (?, ?, ?)",
    ("Alice", 30, "São Paulo")
)
conexao.commit()

cursor.execute("SELECT * FROM pessoas;")
pessoas = cursor.fetchall()
print(pessoas)