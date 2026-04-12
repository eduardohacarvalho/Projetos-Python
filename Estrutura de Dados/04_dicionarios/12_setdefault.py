contato = {"nome": "Eduardo", "telefone": "3333-2221"}

contato.setdefault("nome", "Giovanna")  # "Eduardo"
print(contato)  # {'nome': 'Eduardo', 'telefone': '3333-2221'}

contato.setdefault("idade", 25)  # 25
print(contato)  # {'nome': 'Eduardo', 'telefone': '3333-2221', 'idade': 25}
