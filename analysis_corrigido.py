import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# Permite ao painel do Windows exibir caracteres em UTF-8
sys.stdout.reconfigure(encoding="utf-8")

# Cria a pasta onde os gráficos serão salvos
os.makedirs("Graficos", exist_ok=True)

# =========================================================
# 1. CARREGAMENTO DOS DADOS
# =========================================================

df = pd.read_csv("superstore.csv")

# =========================================================
# 2. LIMPEZA DOS DADOS
# =========================================================

# Remove a coluna desnecessária, caso ela exista
df = df.drop(columns=["记录数"], errors="ignore")

# Converte as colunas de texto para data
df["Order.Date"] = pd.to_datetime(df["Order.Date"])
df["Ship.Date"] = pd.to_datetime(df["Ship.Date"])

# Remove registros duplicados, caso existam
df = df.drop_duplicates()


# =========================================================
# 3. EXPLORAÇÃO DOS DADOS
# =========================================================

print("DIMENSÕES DO DATASET:")
print(df.shape)

print("\nINFORMAÇÕES DO DATASET:")
df.info()

print("\nESTATÍSTICAS DESCRITIVAS:")
print(df.describe())

print("\nVALORES NULOS:")
print(df.isnull().sum())

print("\nCOLUNAS:")
print(df.columns)

print("\nREGISTROS DUPLICADOS:")
print(df.duplicated().sum())

print("\nCATEGORIAS:")
print(df["Category"].unique())

print("\nSEGMENTOS:")
print(df["Segment"].unique())

print("\nMODOS DE ENVIO:")
print(df["Ship.Mode"].unique())

# =========================================================
# 4. INDICADORES GERAIS
# =========================================================

vendas_totais = df["Sales"].sum()
lucro_total = df["Profit"].sum()

print("\nVENDAS TOTAIS:")
print(vendas_totais)

print("\nLUCRO TOTAL:")
print(round(lucro_total, 2))

# =========================================================
# 5. ANÁLISES DE NEGÓCIO
# =========================================================

vendas_categoria = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

lucro_categoria = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

vendas_ano = (
    df.groupby("Year")["Sales"]
    .sum()
    .sort_index()
)

lucro_ano = (
    df.groupby("Year")["Profit"]
    .sum()
    .sort_index()
)

vendas_pais = (
    df.groupby("Country")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

lucro_pais = (
    df.groupby("Country")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

lucro_regiao = (
    df.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

vendas_segmento = (
    df.groupby("Segment")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

produtos_vendas = (
    df.groupby("Product.Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

produtos_lucro = (
    df.groupby("Product.Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

vendas_cidade = (
    df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

lucro_cidade = (
    df.groupby("City")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

lucro_medio_desconto = (
    df.groupby("Discount")["Profit"]
    .mean()
)

frete_medio = (
    df.groupby("Ship.Mode")["Shipping.Cost"]
    .mean()
    .sort_values(ascending=False)
)

print("\nVENDAS POR CATEGORIA:")
print(vendas_categoria)

print("\nLUCRO POR CATEGORIA:")
print(lucro_categoria)

print("\nVENDAS POR ANO:")
print(vendas_ano)

print("\nLUCRO POR ANO:")
print(lucro_ano)

print("\nTOP 10 PAÍSES POR VENDAS:")
print(vendas_pais.head(10))

print("\nTOP 10 PAÍSES POR LUCRO:")
print(lucro_pais.head(10))

print("\nLUCRO POR REGIÃO:")
print(lucro_regiao)

print("\nVENDAS POR SEGMENTO:")
print(vendas_segmento)

print("\nTOP 10 PRODUTOS POR VENDAS:")
print(produtos_vendas.head(10))

print("\nTOP 10 PRODUTOS POR LUCRO:")
print(produtos_lucro.head(10))

print("\nTOP 10 CIDADES POR VENDAS:")
print(vendas_cidade.head(10))

print("\nTOP 10 CIDADES POR LUCRO:")
print(lucro_cidade.head(10))

print("\nLUCRO MÉDIO POR DESCONTO:")
print(lucro_medio_desconto)

print("\nCUSTO MÉDIO DE ENVIO:")
print(frete_medio)


print("Salvando CSV novo...")
df.to_csv("superstore_limpo.csv", index=False, sep=";", encoding="utf-8-sig"
)
#salvar o dataset limpo em csv

# =========================================================
# 6. GRÁFICOS
# =========================================================

# Gráfico 1 - Lucro por categoria
plt.figure(figsize=(8,5))
ax = lucro_categoria.plot(
kind="bar",
color=["royalblue", "orange","green"]
)
plt.title("Lucro por Categoria", fontsize=16)
plt.xlabel("Categoria", fontsize=12)
plt.ylabel("Lucro (USD$)", fontsize=12)
plt.xticks(rotation=0)

# Adiciona o valor em cada barra
for barra in ax.patches:
    altura = barra.get_height()

    ax.annotate(
        f'$ {altura:,.0f}'.replace(",", "."),
        (barra.get_x() + barra.get_width() / 2, altura),
        ha="center",
        va="bottom",
        fontsize=10
    )
plt.tight_layout()
plt.savefig(
"Graficos/lucro_por_categoria_profissional.png",
dpi=300,
bbox_inches="tight"
)
plt.show()
plt.close()

# Gráfico 2 - Vendas por ano
plt.figure(figsize=(8,5))

ax = vendas_ano.plot(
    kind="line",
    marker="o",
    linewidth=3,
    markersize=8,
    color="royalblue"
)

plt.title("Vendas por Ano", fontsize=16)
plt.xlabel("Ano", fontsize=12)
plt.ylabel("Vendas (USD$)", fontsize=12)

plt.grid(alpha=0.3)

for x, y in zip(vendas_ano.index, vendas_ano.values):
    plt.text(x, y, f"{y:,.0f}",
    ha="center",
    va="bottom",
    fontsize=9)

plt.tight_layout()

plt.savefig(
    "Graficos/vendas_por_ano_profissional.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# Gráfico 3 - Lucro por ano
plt.figure(figsize=(8,5))
ax = lucro_ano.plot(
    kind="line",
    marker="o",
    linewidth=3,
    markersize=8,
    color="green"
)
plt.title("Lucro por Ano", fontsize=16)
plt.xlabel("Ano", fontsize=12)
plt.ylabel("Lucro (USD$)", fontsize=12)
plt.grid(alpha=0.3)
for x, y in zip(lucro_ano.index, lucro_ano.values):
    plt.text(
        x,
        y,
        f'$ {y:,.0f}'.replace(",", "."),
        ha="center",
        va="bottom",
        fontsize=9
    )
plt.tight_layout()
plt.savefig(
    "Graficos/lucro_por_ano_profissional.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# Gráfico 4 - Top 10 países por vendas
top10_paises = vendas_pais.head(10).sort_values()
plt.figure(figsize=(10, 6))
ax = top10_paises.plot(
    kind="barh"
)
plt.title("Top 10 Países com Maior Faturamento", fontsize=16)
plt.xlabel("Vendas (USD$)", fontsize=12)
plt.ylabel("País", fontsize=12)
for barra in ax.patches:
    largura = barra.get_width()
    ax.annotate(
        f'$ {largura:,.0f}'.replace(",", "."),
        (largura, barra.get_y() + barra.get_height() / 2),
        ha="left",
        va="center",
        fontsize=9
    )
plt.tight_layout()
plt.savefig(
    "Graficos/top10_paises_profissional.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# Gráfico 5 - Top 10 cidades por vendas
top10_cidades = vendas_cidade.head(10).sort_values()
plt.figure(figsize=(10,6))
ax = top10_cidades.plot(
    kind="barh",
    color="royalblue"
)
plt.title("Top 10 Cidades com Maior Faturamento", fontsize=16)
plt.xlabel("Vendas (USD$)", fontsize=12)
plt.ylabel("Cidade", fontsize=12)
for barra in ax.patches:
    largura = barra.get_width()
    ax.annotate(
        f'$ {largura:,.0f}'.replace(",", "."),
        (largura, barra.get_y() + barra.get_height()/2),
        ha="left",
        va="center",
        fontsize=9
    )
plt.tight_layout()
plt.savefig(
    "Graficos/top10_cidades_profissional.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# Gráfico 6 - Vendas por segmento
plt.figure(figsize=(8, 5))
ax = vendas_segmento.plot(
    kind="bar",
    color=["royalblue", "orange", "green"]
)
plt.title("Vendas por Segmento", fontsize=16)
plt.xlabel("Segmento", fontsize=12)
plt.ylabel("Vendas (USD$)", fontsize=12)
plt.xticks(rotation=0)
for barra in ax.patches:
    altura = barra.get_height()
    ax.annotate(
        f'$ {altura:,.0f}'.replace(",", "."),
        (barra.get_x() + barra.get_width() / 2, altura),
        ha="center",
        va="bottom",
        fontsize=10
    )
plt.tight_layout()
plt.savefig(
    "Graficos/vendas_por_segmento_profissional.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# Gráfico 7 - Top 10 produtos por vendas
top10_produtos = produtos_vendas.head(10).sort_values()
plt.figure(figsize=(12, 6))
ax = top10_produtos.plot(
    kind="barh"
)
plt.title("Top 10 Produtos Mais Vendidos", fontsize=16)
plt.xlabel("Vendas (USD$)", fontsize=12)
plt.ylabel("Produto", fontsize=12)
for barra in ax.patches:
    largura = barra.get_width()
    ax.annotate(
        f'$ {largura:,.0f}'.replace(",", "."),
        (largura, barra.get_y() + barra.get_height() / 2),
        ha="left",
        va="center",
        fontsize=9
    )
plt.tight_layout()
plt.savefig(
    "Graficos/top10_produtos_profissional.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# Gráfico 8 - Lucro médio por desconto
plt.figure(figsize=(10,5))
ax = lucro_medio_desconto.plot(
    kind="line",
    marker="o",
    linewidth=3,
    markersize=8,
    color="crimson"
)
plt.title("Lucro Médio por Desconto", fontsize=16)
plt.xlabel("Desconto", fontsize=12)
plt.ylabel("Lucro Médio (USD$)", fontsize=12)
plt.grid(alpha=0.3)
for x, y in zip(lucro_medio_desconto.index, lucro_medio_desconto.values):
    plt.text(
        x,
        y,
        f'$ {y:,.0f}'.replace(",", "."),
        ha="center",
        va="bottom",
        fontsize=8
    )
plt.tight_layout()
plt.savefig(
    "Graficos/lucro_medio_por_desconto_profissional.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

print("\nProjeto executado com sucesso.")
print("O arquivo superstore_limpo.csv foi criado.")
print("Os gráficos foram salvos na pasta Graficos.")
