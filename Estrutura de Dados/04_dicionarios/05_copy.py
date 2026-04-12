contatos = {"eduardo@gmail.com": {"nome": "Eduardo", "telefone": "3333-2221"}}

copia = contatos.copy()
copia["eduardo@gmail.com"] = {"nome": "Edu"}

print(contatos["eduardo@gmail.com"])  # {"nome": "Eduardo", "telefone": "3333-2221"}

print(copia["eduardo@gmail.com"])  # {"nome": "Edu"}
