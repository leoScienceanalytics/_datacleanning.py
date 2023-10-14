import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# criando um DataFrame com 30 transações aleatórias
df = pd.DataFrame({
    'ID da transação': range(1, 31),
    'Valor da transação': [100, 200, 150, 500, 300, 913, 250, 400, 200, 150, 
                           200, 200, 400, 300, 150, 301, 805, 300, 400, 250, 
                           150, 100, 500, 600, 200, 350, 100, 250, 800, 250],
    'Data da transação': pd.date_range(start='2022-01-01', end='2022-01-30', freq='D'),
    'Local da transação': ['São Paulo, Brasil', 'Rio de Janeiro, Brasil', 'Belo Horizonte, Brasil', 'São Paulo, Brasil', 
                           'São Paulo, Brasil', 'Nova Iorque, EUA', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil',
                           'Rio de Janeiro, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil',
                           'São Paulo, Brasil', 'São Paulo, Brasil', 'Los Angeles, EUA', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil',
                           'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil',
                           'São Paulo, Brasil', 'São Paulo, Brasil', 'Miami, EUA', 'São Paulo, Brasil']
})

print(df)
print(df.describe())

sns.boxplot(x=df['Valor da transação'])
plt.show()

def cal_outliers(coluna, df):
    q1 = df[coluna].quantile(.25) #Quartil 1 (25% dos menores valores da amostra estão nesse Q1)
    q3 = df[coluna].quantile(.75) #Quartil 3 (25% dos maiores valores da amostra estão nesse Q3)
    iqr = q3-q1 #Intervalor InterQuatil

    li = q1 - 1.5*iqr #Limite Inferior
    ls = q3 + 1.5*iqr #Limite Superior

    outliers = (df['Valor da transação'] < li) | (df['Valor da transação'] > ls) #Cria um filtro que retorna em booleano de acordo com a configuração da desigualdade
    return outliers

valortransacao = 'Valor da transação'
outliers = cal_outliers(valortransacao, df)
print(outliers)
print(df[outliers]['Valor da transação'])#Mostrar Outliers da coluna 'cliente.tempo_servico'.
print(df[outliers])

