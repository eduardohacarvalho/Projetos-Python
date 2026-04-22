import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)
print(df.head())
print("\n\n df.info")
print(df.info())
print("\n\n df.describe")
print(df.describe())
print("\n\n\n\n Campos em branco")
print(df.isnull().sum())

df_limpo = df.dropna()

df["Age"] = df["Age"].fillna(df["Age"].mean())

df["Age_log"] = df["Age"].apply(lambda x: x)
print(df["Age_log"])

df["Fare_normalized"] = (df["Fare"] - df["Fare"].min()) / (df["Fare"].max() - df["Fare"].min())
print(df.head)

def limpar_dados(df):
    df["Age"] = df["Age"].fillna(df["Age"].mean(), inplace=True)

    df["Fare_normalized"] = (df["Fare"] - df["Fare"].min()) / (df["Fare"].max() - df["Fare"].min())
    return df

def validar_dataset(df):
    print("Linhas: ", df.shape[0])
    print("Colunas: ", df.shape[1])
    print("\nValores ausentes: ")
    print(df.isnull().sum())

validar = validar_dataset(df)
print(validar)
    
