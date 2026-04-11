# Lê o valor total da compra como inteiro
valor_compra = int(input())

# TODO: Implemente a estrutura condicional para decidir e imprimir a mensagem correta
# Dica: Use if, elif e else para comparar o valor_compra com as faixas especificadas no enunciado.
if valor_compra < 50:
  print("Obrigado por comprar conosco!")
elif valor_compra < 100 and valor_compra >= 50:
  print("Parabens! Voce ganhou um brinde!")
elif valor_compra >= 100 and valor_compra < 200:
  print("Desconto de 10 reais aplicado!")
else:
  print("Desconto de 25 reais aplicado!")