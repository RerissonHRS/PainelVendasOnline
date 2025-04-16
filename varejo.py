import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Painel de Vendas On-line S.A.", layout="wide")

# Funcão para gerar dados de exemplo

@st.cache_data
def generate_data():
    np.random.seed(42)

    # Vendas diárias
    data = pd.DataFrame({
        "Data": pd.date_range(start="2023-01-01", end="2023-12-31", freq="D"),
        "Vendas": np.random.randint(1000, 5000, 365),
        "Categoria": np.random.choice(["Eletrônicos", "Roupas", "Livro", "Casa", "Esportes"], 365),
    })

    # Dados de clientes
    df_clientes = pd.DataFrame({
        "Data": pd.date_range(start="2023-01-01", end="2023-12-31", freq="D"),
        "Novos_Clientes": np.random.randint(10, 100, 365),
        "Satisfacao": np.random.uniform(5.0, 13.5, 365),  # Corrigido para garantir o intervalo correto
    })

    # Dados de produtos
    df_produtos = pd.DataFrame({
        "Produto": ["Smartphone", "Notbook", "Tênis", "Livro", "Camiseta"],
        "Vendas": [15000, 12000, 9000, 7500, 6000],  # Usando lista fixa em vez de randint com múltiplos argumentos
        "Avaliacoes": [4.5, 4.3, 4.2, 4.7, 4.1],      # Também como lista direta
        "Categoria": ["Eletrônicos", "Eletrônicos", "Esportes", "Livros", "Roupas"],
    })

    return data, df_clientes, df_produtos

# Carregando os dados
df_vendas, df_clientes, df_produtos = generate_data()

# Sidebar para filtros
st.sidebar.header("Filtros")
categoria_selecionada = st.sidebar.multiselect("Selecionar Categoria:", options=df_vendas["Categoria"].unique(), default=df_vendas["Categoria"].unique())

# Filtrar Dados
df_vendas_filtrado = df_vendas[df_vendas["Categoria"].isin(categoria_selecionada)]
df_produtos_filtrado = df_produtos[df_produtos["Categoria"].isin(categoria_selecionada)]

# Título do Painel
st.title("Painel de Vendas On-line S.A.")
st.markdown("## Análise de Vendas e Clientes")

# Métricas principais

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Vendas", f"R$ {df_vendas_filtrado['Vendas'].sum():,.2f}")
with col2:
    st.metric("Novos Clientes", df_clientes["Novos_Clientes"].sum())
with col3:
    st.metric("Satisfação Média", f"{df_clientes['Satisfacao'].mean():.2f}")

# gráfico de Vendas ao longo do tempo
st.subheader("Vendas ao longo do tempo")
fig_vendas_tempo = px.line(df_vendas_filtrado, x="Data", y="Vendas")
st.plotly_chart(fig_vendas_tempo, use_container_width=True)

# Gráfico de Vendas por Categoria
st.subheader("Vendas por Categoria")
df_cat = df_vendas_filtrado.groupby("Categoria")["Vendas"].sum().reset_index()
fig_vendas_categoria = px.pie(df_cat, values="Vendas", names="Categoria")
st.plotly_chart(fig_vendas_categoria, use_container_width=True)

# Gráficos de novos clientes e satisfação
col1, col2 = st.columns(2)
with col1:
    st.subheader("Novos Clientes por Dia")
    fig_novos_clientes = px.bar(df_clientes, x="Data", y="Novos_Clientes")
    st.plotly_chart(fig_novos_clientes, use_container_width=True)
with col2:
    st.subheader("Satisfação dos Clientes ao longo do tempo")
    fig_satisfacao_tempo = px.line(df_clientes, x="Data", y="Satisfacao")
    st.plotly_chart(fig_satisfacao_tempo, use_container_width=True)

#Gráfico de top produtos
st.subheader("Top Produtos: Vendas vs. Avaliação")
fig_top_produtos = px.scatter(df_produtos_filtrado, x="Vendas", y="Avaliacoes", color="Produto", size="Vendas", text="Produto", title="Top Produtos: Vendas vs Avaliação")
fig_top_produtos.update_traces(textposition="top center")
st.plotly_chart(fig_top_produtos, use_container_width=True)

# Tabela de Dados
st.subheader("Tabela de Vendas Filtradas")
tab1, tab2, tab3 = st.tabs(["Vendas","Clientes", "Produtos"])

with tab1:
    st.dataframe(df_vendas_filtrado)
with tab2:
    st.dataframe(df_clientes)
with tab3:
    st.dataframe(df_produtos_filtrado)

# Conclusão e Recomendações
st.markdown("## Conclusões e Recomendações")

st.markdown("""
### 🔍 Conclusões:

- As **vendas totais** no período analisado foram significativas, ultrapassando **R$ {:,.2f}**, com destaque para a categoria **{}**.
- O número total de **novos clientes** foi de **{}**, indicando um bom crescimento da base de consumidores.
- A **satisfação média dos clientes** se manteve em **{:.2f}**, sugerindo uma experiência positiva para a maioria.
- O produto com maior volume de vendas foi **{}**, enquanto o mais bem avaliado foi **{}** com nota média de **{}**.

### 💡 Recomendações:

- **Investir mais em marketing** nas categorias com maior retorno de vendas para potencializar os lucros.
- **Analisar categorias com menor desempenho** (como {}), a fim de reavaliar mix de produtos ou estratégias de precificação.
- **Monitorar a satisfação dos clientes** e coletar feedbacks mais específicos, visando manter ou melhorar os índices atuais.
- **Focar em produtos bem avaliados**, pois há maior chance de fidelização e recomendação boca a boca.

""".format(
    df_vendas_filtrado['Vendas'].sum(),
    df_vendas_filtrado.groupby("Categoria")["Vendas"].sum().idxmax(),
    df_clientes["Novos_Clientes"].sum(),
    df_clientes["Satisfacao"].mean(),
    df_produtos_filtrado.sort_values("Vendas", ascending=False)["Produto"].iloc[0],
    df_produtos_filtrado.sort_values("Avaliacoes", ascending=False)["Produto"].iloc[0],
    df_produtos_filtrado["Avaliacoes"].max(),
    df_vendas_filtrado.groupby("Categoria")["Vendas"].sum().idxmin()
))