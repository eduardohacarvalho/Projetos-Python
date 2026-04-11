# reverse

linguagem = ["python", "js", "c", "java", "csharp"]

linguagem.reverse()

print(linguagem)  # ["csharp", "java", "c", "js", "python"]

# sort

linguagens = ["python", "js", "c", "java", "csharp"]
linguagens.sort()  # ["c", "csharp", "java", "js", "python"]
print(linguagens)

linguagens = ["python", "js", "c", "java", "csharp"]
linguagens.sort(reverse=True)  # ["python", "js", "java", "csharp", "c"]
print(linguagens)

linguagens = ["python", "js", "c", "java", "csharp"]
linguagens.sort(key=lambda x: len(x))  # ["c", "js", "java", "python", "csharp"]
print(linguagens)

linguagens = ["python", "js", "c", "java", "csharp"]
linguagens.sort(key=lambda x: len(x), reverse=True)  # ["python", "csharp", "java", "js", "c"]
print(linguagens)

# len
linguagens_len = ["python", "js", "c", "java", "csharp"]

print(len(linguagens_len))  # 5

# Sorted

linguagens_x = ["python", "js", "c", "java", "csharp"]

print(sorted(linguagens_x, key=lambda x: len(x)))  # ["c", "js", "java", "python", "csharp"]
print(sorted(linguagens_x, key=lambda x: len(x), reverse=True))  # ["python", "csharp", "java", "js", "c"]