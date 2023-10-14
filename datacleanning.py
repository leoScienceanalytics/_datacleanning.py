#Data Cleanning
#Acessando JSON dentro de colunas do DataFrame
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt

#Importando o dataset
df = pd.read_json('basededados.json')
print(df.head(5))


#Limpando os dados
#Transformando dados em uma tabela
with open ('basededados.json') as f: #Chama o json de f e abre ele
    json_bruto = json.load(f) #carrega o json f, e nomeia como json_bruto

df = pd.json_normalize(json_bruto) #normaliza o json_bruto e chama esse df 'dfnorm'
print(df)

colunas = df.columns #Criar variável que contém as colunas do dataframe 'dfnorm'
colunmslist = colunas.tolist() #Listar de forma organizada 
print('Lista de colunas do dataframe: ', colunmslist)

#Entendendo os dados
print(df.info()) #Informação comportamental de cada coluna

#Identificando dados vazios
print('A: ', df[df['conta.cobranca.Total'] == ' ']) #Mostrar linhas em que a coluna 'conta.cobranca.Total' está com os campos vazios
print(df[df['conta.cobranca.Total'] == ' '][['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']])


idx = df[df['conta.cobranca.Total'] == ' '].index #Mostrar o valor do index (Linha) onde está com celular vazia na coluna 'conta.cobranca.Total'
df.loc[idx, 'conta.cobranca.Total'] = df.loc[idx, 'conta.cobranca.mensal'] * 24 #Realizar cálculo dos valores que estão ausentes
print('conta.cobranca.Total: ',df.loc[idx, 'conta.cobranca.Total'] )

df.loc[2075, 'conta.contrato'] = 'dois anos' #Trocando uma valor específico
df.loc[idx, 'cliente.tempo_servico'] = 24 #Dando valor a todos as células da coluna e índice em questão

print(df.loc[idx][['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']])
df['conta.cobranca.Total'] = df['conta.cobranca.Total'].astype(float) #Trandofrmando a coluna em float
print(df.info()) #Verificando o formato em que os dados estão


for col in df.columns: #Valores col nas colunas do dfnorm, iterar:
    print(f'coluna: {col}') #Os nomes das colunas
    print(df[col].unique()) #Os valores únicos
    print('-'*30)
    
print(df.query("Churn == ''")) #Filtrando dados para mostrar somente os valores onde o churn está vazio


#Criando uma df cópia
df = df[df['Churn'] != ''] #DataFrame modificado, atual
print(df)
print(df.info()) 
print(df.reset_index(drop=True, inplace=True)) #Remove o Index do dataframe
print(df)

#Identificando e removendo dados duplicados
duplicadas = df.duplicated() #Verificando se há duplicadas, retorna em Booleano
print( duplicadas)
somaduplicadas = duplicadas.sum() #Verificando a soma das duplicadas
print(somaduplicadas)
print(df[duplicadas]) #Retorna somente as True de duplicadas   
df.drop_duplicates(inplace=True) #Dropando duplicadas do dataframe 'dfnorm1'
print(df.duplicated())
print(df.duplicated().sum())

#Identificando e substituindo dados nulos
print(df.isna()) #método que mostra quais são os valores nulos, retorna em Booleano
print(df.isna().sum()) #Soma de nulos por coluna
print(df.isna().sum().sum()) #Soma de nulos totais

print(df[df.isna().any(axis=1)]) #Filtra para achar valores que possuem valores nulos em pelo menos uma das colunas


filtro = df['cliente.tempo_servico'].isna() #Cria filtro de dados nulos
print(df[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]) #Mostrar o filtro aplicados as colunas em questão
df['cliente.tempo_servico'].fillna( #Vai calcular os valores da coluna 'cliente.tempo_servico' usando o fillna(), fillna() é usado para preencher os valores NaN
    np.ceil(
        df['conta.cobranca.Total'] / df['conta.cobranca.mensal']
    ), inplace=True
)  

print(df[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]) #Mostrar o filtro aplicados as colunas em questão
print(df.isna().sum()) #Soma de nulos por coluna

#Remoção dos dados nulos
colunadropar= ['conta.contrato', 'conta.faturamente_eletronico', 'conta.metodo_pagamento']
print(df[colunadropar].isna().any(axis=1).sum())
df = df.dropna(subset=colunadropar) #DataFrame modificado, atual
print(df.head())
print(df.isna().sum())
print(df.reset_index(drop=True, inplace=True))
print(df)

#Tratando Outliners/Outliers
print(df.describe())

#Boxplot
sns.boxplot(x=df['cliente.tempo_servico'])
plt.show()

q1 = df['cliente.tempo_servico'].quantile(.25) #Quartil 1 (25% dos menores valores da amostra estão nesse Q1)
q3 = df['cliente.tempo_servico'].quantile(.75) #Quartil 3 (25% dos maiores valores da amostra estão nesse Q3)
iqr = q3-q1 #Intervalor InterQuatil

li = q1 - 1.5*iqr #Limite Inferior
ls = q3 + 1.5*iqr #Limite Superior

outliers = (df['cliente.tempo_servico'] < li) | (df['cliente.tempo_servico'] > ls) #Cria um filtro que retorna em booleano de acordo com a configuração da desigualdade
print(outliers)

print(df[outliers]['cliente.tempo_servico']) #Mostrar Outliers da coluna 'cliente.tempo_servico'.

df.loc[outliers, 'cliente.tempo_servico'] = np.ceil(
    df.loc[outliers, 'conta.cobranca.Total'] / df.loc[outliers, 'conta.cobranca.mensal']
) #Calcula e preenche os valores onde estão os Outliers

sns.boxplot(x=df['cliente.tempo_servico']) #Nova Boxplot de verificação
plt.show() #Visualização, tentativa de retirar todos Outliers deu erro.
print(df)

outliers = (df['cliente.tempo_servico'] < li) | (df['cliente.tempo_servico'] > ls) #Coluna foi atualizada, logo, quando filtrada, somente os quatro Outliers restantes aparecerão.
print(df[outliers])

df = df[~outliers]
print(df)

sns.boxplot(x=df['cliente.tempo_servico'])
plt.show()
outliers = (df['cliente.tempo_servico'] < li) | (df['cliente.tempo_servico'] > ls)
print(outliers)
print(df.reset_index(drop=True, inplace=True))
print(df.describe())
print(df)



#Variáveis Categóricas
df = df.drop('id_cliente', axis=1)
print(df)

mapeamento = {
    'nao': 0,
    'sim': 1,
    'masculinao': 0,
    'feminino': 1
}
for col in df.columns: #Chama de col e  acessa  as colunas no dataframe df
    print(f'Coluna: {col}') #Printa os nomes das colunas do dataframe df
    print(df[col].unique()) #Printa as valores únicos de cada coluna
    print('-'*30)