frutas = ["laranja", "maca", "uva", "pera"]
print(frutas)

frutas = []
print(frutas)

letras = list("python")
print(letras)

numeros = list(range(10))
print(numeros)

carro = ["Ferrari", "F8", 4200000, 2020, 2900, "São Paulo", True]
print(carro)

frutas = ["laranja", "maca", "uva", "pera"]

#Acesso direto a lista declarada "Frutas"
print(frutas[0])  # laranja
print(frutas[2])  # uva

#Indices negativos
print(frutas[-1])  # pera
print(frutas[-3])  # maca

# FATIAMENTO DE LISTA
lista = ["p", "y", "t", "h", "o", "n"]

print(lista[2:])  # ["t", "h", "o", "n"]
print(lista[:2])  # ["p", "y"]
print(lista[1:3])  # ["y", "t"]
print(lista[0:3:2])  # ["p", "t"]
print(lista[::])  # ["p", "y", "t", "h", "o", "n"]
print(lista[::-1])  # ["n", "o", "h", "t", "y", "p"]