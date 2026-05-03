import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

url = 'https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv'
df = pd.read_csv(url)
print(df.head())

df = df.dropna()

df_class = df.copy()
df_class['HighPrice'] = (
    df_class['median_house_value'] > 
    df_class['median_house_value'].median()
).astype(int)

print(df_class.head())

x = df_class.drop(['median_house_value', "HighPrice"], axis=1)
x = pd.get_dummies(x)
y = df_class['HighPrice']

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

#Regressão Logística
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(max_iter=1000)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)

# Matriz de Confusão
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
)
plt.xlabel('Classe Predita')
plt.ylabel('Classe Real')
plt.title('Matriz de Confusão')
plt.show()

# Acuracia
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print(f'Acurácia: {accuracy:.2f}')

# Precision
from sklearn.metrics import precision_score
precision = precision_score(y_test, y_pred)
print(f'Precision: {precision:.2f}')

# Recall
from sklearn.metrics import recall_score
recall = recall_score(y_test, y_pred)
print(f'Recall: {recall:.2f}')

# F1-Score
from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_pred)
print(f'F1-Score: {f1:.2f}')

from sklearn.metrics import classification_report
report = classification_report(y_test, y_pred)
print('Classification Report:')
print(report)

# Tecnicas de Clustering - Within Sum of Squares (WSS)
from sklearn.cluster import KMeans
wcss = []
K = range(1, 10)
for k in K:
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(x)
    wcss.append(model.inertia_)


plt.plot(K, wcss, marker='o')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('WSS')
plt.title('Elbow Method')
plt.show()