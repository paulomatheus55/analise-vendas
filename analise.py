from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ARQUIVO_DADOS = Path("dados/vendas.csv")
PASTA_GRAFICOS = Path("graficos")
PASTA_RELATORIOS = Path("relatorios")

def formatar_reais(valor):
    ## Converte 1234.5 em R$ 1.234,50 ##
    texto = f"R$ {valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def carregar_dados():
    ## Carrega os dados do arquivo CSV ##
    return pd.read_csv(caminho, parse_dates=["data"])


def limpar_dados(df):
    ## Remove duplicatas, vazios e cria colunas novas ##
    df = df.drop_duplicates().copy()
    df["regiao"] = df["regiao"].fillna("Não informado")
    df["receita"] = df["quantidade"] * df["preco_unitario"]
    df["mes"] = df["data"].dt.to_period("M").astype(str)
    return df


def calcular_metricas(df):
    ## Calcula métricas de vendas ##
    return {
        "Total de vendas": len(df),
        "Receita total": df["receita"].sum(),
        "Ticket médio": df["receita"].mean(),
    }


def receita_por(df, coluna):
    ## Soma a receita e agrupa por uma coluna específica ##
    return df.grupby(coluna)["receita"].sum()