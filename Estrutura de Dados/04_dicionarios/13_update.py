contatos = {"eduardo@gmail.com": {"nome": "Eduardo", "telefone": "3333-2221"}}

contatos.update({"eduardo@gmail.com": {"nome": "Edu"}})
print(contatos)  # {'eduardo@gmail.com': {'nome': 'Edu'}}

contatos.update({"giovanna@gmail.com": {"nome": "Giovanna", "telefone": "3322-8181"}})
# {'guilherme@gmail.com': {'nome': 'Gui'}, 'giovanna@gmail.com': {'nome': 'Giovanna', 'telefone': '3322-8181'}}
print(contatos)
