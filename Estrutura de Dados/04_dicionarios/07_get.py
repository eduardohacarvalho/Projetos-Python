contatos = {"eduardo@gmail.com": {"nome": "Eduardo", "telefone": "3333-2221"}}

# contatos["chave"]  # KeyError

resultado = contatos.get("chave")  # None
print(resultado)

resultado = contatos.get("chave", {})  # {}
print(resultado)

resultado = contatos.get(
    "eduardo@gmail.com", {}
)  # {"eduardo@gmail.com": {"nome": "Eduardo", "telefone": "3333-2221"}
print(resultado)
