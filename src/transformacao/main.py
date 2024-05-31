# importacao das ferramentas 
import pandas as pd
import sqlite3
from datetime import datetime

# definir o caminho para o arquivo jsonl
df = pd.read_json('../data/data.jsonl',lines=True)
print(df)

# setar o pandas para mostrar todas as colunas 

pd.options.display.max_columns = None

# adicionar coluna source com o caminho fixo 

df['_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

# adicionar coluna com a data e hora da coleta 

df['_data_coleta'] = datetime.now()

print(df)

# tratar valores numericos e de texto - transforma a coluna para a própria coluna com o tipo float

df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_cents'] = df['old_price_cents'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_cents'] = df['new_price_cents'].fillna(0).astype(float)
df['reviwes_rating_number'] = df['reviwes_rating_number'].fillna(0).astype(float)

# remover parenteses da coluna reviews_amount e tipar os dados para o tipo int

df['reviwes_amount'] = df['reviwes_amount'].str.replace('[\(/)]','',regex=True)
df['reviwes_amount'] = df['reviwes_amount'].fillna(0).astype(int)

# tratar os preços como float e calcular os valores totais

df['old_price'] = df['old_price_reais'] + df['old_price_cents'] / 100 
df['new_price'] = df['new_price_reais'] + df['new_price_cents'] / 100

# remover as colunas antigas de preço 

df.drop(columns=['old_price_reais', 'old_price_cents', 'new_price_reais', 'new_price_cents'], inplace=True)

# conectar ao banco de dados sqlite3

conn = sqlite3.connect('../data/quotes.db')

# salvar o dataframe no banco de dados Sqlite

df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# fechar a conexao com o banco de dados

conn.close()

print(df.head())