import pandas as pd
import numpy as np
import json

df = pd.read_json('baseexerc.json')
print(df) #Há colunas dentro de outras colunas

with open ('baseexerc.json') as f:
    json_novo = json.load(f)
    
df = pd.json_normalize(json_novo)
print(df)

colunas = df.columns
listacolunas = colunas.tolist()
print(listacolunas)

print(df.info())
print('Não Nulos:', df.isna())

#Removendo dados nulos
filtro = ['carga_horaria','concluintes', 'data_inicio', 'data_conclusao', 'descricao', 'preco']
print(df[filtro]) #Filtragem de colunas
df.drop(1, inplace=True) #Exclui a linha interia de Nulo, no caso era a linha 1
df.reset_index(drop=True, inplace=True) #Resetando o index do dataframe e consolidando
print(df)


#Removendo vazios
filtrovazio= ['concluintes', 'data_inicio', 'data_conclusao', 'descricao', 'preco', 'instrutor.nome', 'instrutor.email', 'instrutor.telefone']
print(df[filtrovazio])
print(df.info())
print('Não Nulos:', df.isna())
df.drop(2, inplace=True)
df.drop(3, inplace=True)
df.reset_index(drop=True, inplace=True)
print(df[filtrovazio])

filtroobj = ['preco', 'concluintes'] # Não consegue converveter pois há valores incorretos no dataframe
df[filtroobj] = df[filtroobj].astype(float) #Transformando coluna em string
print(df.info())
print(df)
print(df.isna())