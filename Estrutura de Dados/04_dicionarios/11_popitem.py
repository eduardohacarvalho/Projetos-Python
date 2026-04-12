contatos = {"eduardo@gmail.com": {"nome": "Eduardo", "telefone": "3333-2221"}}

resultado = contatos.popitem()  # ('eduardo@gmail.com', {'nome': 'Eduardo', 'telefone': '3333-2221'})
print(resultado)

# contatos.popitem()  # KeyError
