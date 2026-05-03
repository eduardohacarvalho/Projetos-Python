import pandas as pd

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
df = pd.read_csv(url)

print(df.head(10))

import matplotlib.pyplot as plt

plt.scatter(df['total_bill'], df['tip'])
plt.xlabel('Conta Total')
plt.ylabel('Valor da Gorjeta')
plt.title('Relação entre Conta e Gorjeta')

plt.show()

import plotly.express as px

fig = px.scatter(
    df,
    x='total_bill',
    y='tip',
    color='day',
    title='Relação entre Conta e Gorjeta'
)

fig.show()

plt.figure(figsize=(8, 5))

plt.bar(df['day'], df['tip'], color='skyblue')

plt.title('Gorjetas por dia da semana')

plt.xlabel('Dia da Semana')
plt.ylabel('Valor da Gorjeta')

plt.show()

fig, ax = plt.subplots(1,2, figsize=(10,4))

import seaborn as sns

sns.histplot(df['total_bill'], ax=ax[0])
ax[0].set_title('Distribuição da Conta')

sns.boxplot(data=df, x='day', y='tip', ax=ax[1])
ax[1].set_title('Gorjetas por dia')

plt.show()

fig = px.scatter(
    df,
    x='total_bill',
    y='tip',
    color='day',
    size='size',
    title='Relação entre Conta e Gorjeta'
)
fig.show()

correlacao = df.corr(numeric_only=True)
plt.figure(figsize=(8, 6))

sns.heatmap(
    correlacao,
    annot=True,
    cmap='coolwarm'
)
plt.title('Mapa de Calor das Correlações')
plt.show()