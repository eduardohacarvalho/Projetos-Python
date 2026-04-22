import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

array = np.array([1, 2, 3, 4, 5])
print("Array NumPy:", array)

dados = {
    "Nome": ["Alice", "Bob", "Charlie"],
    "Idade": [30, 25, 35]
}

df = pd.DataFrame(dados)
print("DataFrame Pandas:")
print(df)

x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 32]
plt.plot(x, y)
# plt.show() # Exibe grafico de X e Y

numeros = np.array([1, 2, 3, 4, 5])
resultado = numeros * 2
print("Resultado da multiplicação por 2:", resultado)

produto = {
    "produto": ["Notebook", "Smartphone", "Tablet"],
    "preço": [2000, 1500, 1000]
}
df_produto = pd.DataFrame(produto)
print("DataFrame de Produtos:")
print(df_produto)
df_produto.to_csv("dados.csv", index=False)
print(df_produto["preço"])
print("Média:", df_produto["preço"].mean())
print("Contagem:", df_produto["preço"].count())
print("Máximo:", df_produto["preço"].max())
print("Mínimo:", df_produto["preço"].min())
print("Soma:", df_produto["preço"].sum())
print("Desvio Padrão:", df_produto["preço"].std())
print("Mediana:", df_produto["preço"].median())
print("Moda:", df_produto["preço"].mode()[0])
print("Resumo Estatístico:")
print(df_produto["preço"].describe())

plt.bar(df_produto["produto"], df_produto["preço"])
# plt.show() # Exibe grafico de barras dos produtos e seus preços


prod = {
    "produto": ["Notebook", "Mouse", "Teclado", "Mouse", "Teclado"],
    "preço": [3500, 120, 150, 120, 200]
}
df_prod = pd.DataFrame(prod)
print(df_prod.groupby("produto").mean())