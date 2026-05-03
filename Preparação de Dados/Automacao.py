import csv

total = 0

with open("vendas.txt", "w") as f:
    f.write("100\n200\n150\n300")

with open("vendas.txt", "r") as f:
    for line in f:
        valor = int(line.strip())
        total += valor
print(f"Total das vendas: {total}")

import requests

url = "https://api.agify.io?name=ana"
resposta = requests.get(url)
dados = resposta.json()
print(dados)

