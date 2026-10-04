# APP BASE 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Cibersegurança no Brasil", layout="wide")
sns.set_theme(style="whitegrid")


@st.cache_data
def carregar() -> pd.DataFrame:
    # Cragge o csv n 26 
    df = pd.read_csv("dados/simulacao_ciberseguranca_brasil.csv")
    df["data"] = pd.to_datetime(df["data"])
    return df


dados = carregar()

st.title("Cibersegurança no Brasil (2015–2024)")
st.write(
    "Incidentes cibernéticos (ransomware, phishing, vazamentos etc.) causam "
    "perdas financeiras e paralisam serviços essenciais. Este painel explora "
    "uma base simulada de registros mensais (2015–2024) para identificar "
    "padrões por período, região e setor e apoiar decisões de defesa."
)
st.markdown("---")
st.write(" Matéria: Linguagens de Programação")
st.write(" Aluna: Larissa Villela dos santos")
st.write(" Professor: Alexandre Neves Louzada")
st.markdown("---")



# --------------------------------------------------------- filtros (lateral)
st.sidebar.header("Filtros")
a0, a1 = int(dados["ano"].min()), int(dados["ano"].max())
anos = st.sidebar.slider("Período", a0, a1, (a0, a1))
regioes = st.sidebar.multiselect("Região", sorted(dados["regiao"].unique()),
                                 default=sorted(dados["regiao"].unique()))
ufs_disp = sorted(dados.loc[dados["regiao"].isin(regioes), "uf"].unique())
ufs = st.sidebar.multiselect("UF", ufs_disp, default=ufs_disp)
setores = st.sidebar.multiselect("Setor", sorted(dados["setor"].unique()),
                                 default=sorted(dados["setor"].unique()))

df = dados[dados["ano"].between(*anos) & dados["regiao"].isin(regioes)
           & dados["uf"].isin(ufs) & dados["setor"].isin(setores)]
if df.empty:
    st.warning("Nenhum registro com esses filtros.")
    st.stop()

# -------------------------------------------------------------- indicadores
taxa_resolvido = (df["status_resposta"] == "Resolvido").mean() * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Incidentes", f"{df['incidentes'].sum():,}".replace(",", "."))
c2.metric("Impacto financeiro", f"R$ {df['impacto_financeiro'].sum() / 1e6:,.1f} mi")
c3.metric("Recuperação média", f"{df['tempo_recuperacao'].mean():.1f} h")
c4.metric("Taxa de resolução", f"{taxa_resolvido:.1f} %")

# ----------------------------------------------------------------- graficos
c1, c2 = st.columns(2)

anual = df.groupby("ano")["incidentes"].sum()
fig, ax = plt.subplots(figsize=(7, 4))
anual.plot(ax=ax, marker="o")
ax.set(title="Incidentes por ano", ylabel="Incidentes")
c1.pyplot(fig)

por_ataque = df.groupby("tipo_ataque")["impacto_financeiro"].sum().sort_values() / 1e6
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(por_ataque.index, por_ataque.values, color="#c0392b")
ax.set(title="Impacto por tipo de ataque", xlabel="R$ milhões")
c2.pyplot(fig)

por_regiao = df.groupby("regiao")["incidentes"].sum()
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(por_regiao.index, por_regiao.values, color="#2980b9")
ax.set(title="Incidentes por região", ylabel="Incidentes")
st.pyplot(fig)

# -------------------------------------------------------------------- dados
st.subheader("Resumo por setor")
resumo = df.groupby("setor").agg(
    incidentes=("incidentes", "sum"),
    impacto_mi=("impacto_financeiro", lambda s: s.sum() / 1e6),
    recuperacao_h=("tempo_recuperacao", "mean"),
).round(1).sort_values("impacto_mi", ascending=False)
st.dataframe(resumo)

st.subheader("Dados filtrados")
st.dataframe(df, hide_index=True, height=350)
st.download_button("⬇️ Baixar CSV", df.to_csv(index=False).encode("utf-8"),
                   "ciberseguranca_filtrado.csv", "text/csv")

# ---------------------------------------------------------- interpretacao
top_regiao = df.groupby("regiao")["incidentes"].sum().idxmax()
top_ataque = df.groupby("tipo_ataque")["impacto_financeiro"].sum().idxmax()
top_vuln = df.groupby("vulnerabilidade")["incidentes"].sum().idxmax()
total_inc = f"{df['incidentes'].sum():,}".replace(",", ".")

st.subheader("Interpretação")
st.markdown(f"""
- **{top_regiao}** é a região com mais incidentes no recorte selecionado.
- **{top_ataque}** é o tipo de ataque de maior impacto financeiro acumulado.
- **{top_vuln}** é a vulnerabilidade mais associada aos incidentes.
- Apenas **{taxa_resolvido:.1f}%** dos casos está com status *Resolvido*.
- O volume anual se mantém estável no período — o problema é crônico, não crescente.
""")

st.subheader("Conclusão executiva")
st.markdown(f"""
No recorte filtrado, os incidentes somam
**{total_inc}** ocorrências e
**R$ {df['impacto_financeiro'].sum() / 1e6:,.0f} milhões** em perdas,
com recuperação média de **{df['tempo_recuperacao'].mean():.0f} horas**.
A prioridade de defesa deve ser a região **{top_regiao}** e o vetor
**{top_ataque}**, reduzindo a exposição a **{top_vuln}**
(MFA, política de senhas e atualizações). Como apenas ~1/3 dos casos está
resolvido, recomenda-se investir em planos de resposta a incidentes.

*Base simulada — resultados ilustram a metodologia.*
""")
