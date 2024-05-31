import pandas as pd
import streamlit as st
import sqlite3

#conectar com o banco de dados

conn = sqlite3.connect('../data/quotes.db')

# carregar os dados da tabela do banco em um dataframe pandas

df = pd.read_sql_query("SELECT * FROM mercadolivre_items", conn)

# fechar conexao com o banco de dados
conn.close()

#titulo da aplicacao
st.title('Pesquisa de Mercado - Tênis Esportivos no Mercado Livre')

# Melhorar layout com colunas para kpis
st.subheader('Principais KPIs da Aplicação')
col1, col2, col3 = st.columns(3)

# kpi numero total de itens 
total_itens = df.shape[0]
col1.metric(label='Numero Total de itens', value = total_itens)

# kpi 2 numero de marcas 
unique_brands = df['brand'].nunique()
col2.metric(label='Numero de Marcas', value = unique_brands)

# kpi 3 Preço médio 
price_medio = df['new_price'].mean()
col3.metric(label='Preço Médio (R$)', value =f"{price_medio:.2f}")

# Marcas mais encontradas nas paginas consultadas 
st.subheader('Marcas mais encontradas nas paginas')
col1, col2 = st.columns([4,2])
top_10_pages_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)

# Preco Medio da marca 
st.subheader('Preço Médio por Marca')
col1, col2 = st.columns([4,2])
df_non_zero_prices = df[df['new_price'] > 0]
price_medio_brand = df_non_zero_prices.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(price_medio_brand)
col2.write(price_medio_brand)

# qual a satifação dos clientes por marca
st.subheader('Satisfação por marca')
col1, col2 = st.columns([4,2])
df_non_zero_reviwes = df[df['reviwes_rating_number']>0]
satisfaction_by_brand = df_non_zero_reviwes.groupby('brand')['reviwes_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)