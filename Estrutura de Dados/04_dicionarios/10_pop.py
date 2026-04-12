contatos = {"eduardo@gmail.com": {"nome": "Eduardo", "telefone": "3333-2221"}}

resultado = contatos.pop("eduardo@gmail.com")  # {'nome': 'Eduardo', 'telefone': '3333-2221'}
print(resultado)

resultado = contatos.pop("eduardo@gmail.com", {})  # {}
print(resultado)
