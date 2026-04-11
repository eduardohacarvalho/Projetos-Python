#Count

cores = ["vermelho", "azul", "verde", "azul"]

print(cores.count("vermelho"))  # 1
print(cores.count("azul"))  # 2
print(cores.count("verde"))  # 1

# Extend

linguagens = ["python", "js", "c"]

print(linguagens)  # ["python", "js", "c"]

linguagens.extend(["java", "csharp"])

print(linguagens)  # ["python", "js", "c", "java", "csharp"]

#Index
linguagens2 = ["python", "js", "c", "java", "csharp"]

print(linguagens2.index("java"))  # 3
print(linguagens2.index("python"))  # 0

# pop

linguagens3 = ["python", "js", "c", "java", "csharp"]

print(linguagens3.pop())  # csharp
print(linguagens3.pop())  # java
print(linguagens3.pop())  # c
print(linguagens3.pop(0))  # python

#remove

linguagens.remove("c")

print(linguagens)  # ["python", "js", "java", "csharp"]