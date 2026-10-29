from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ARQUIVO_DADOS = Path("dados/vendas.csv")
PASTA_GRAFICOS = Path("graficos")
PASTA_RELATORIOS = Path("relatorios")


def formatar_reais(valor):
    ## Converte 1234.5 em 'R$ 1.234,50' ##
    texto = f"R$ {valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def carregar_dados(caminho):
    ## Lê o CSV ##
    return pd.read_csv(caminho, parse_dates=["data"])


def limpar_dados(df):
    ## Remove duplicatas, trata vazios e cria colunas novas ##
    df = df.drop_duplicates().copy()
    df["regiao"] = df["regiao"].fillna("Não informado")
    df["receita"] = df["quantidade"] * df["preco_unitario"]
    df["mes"] = df["data"].dt.to_period("M").astype(str)
    return df


def calcular_metricas(df):
    ## Calcula os indicadores principais do negócio ##
    return {
        "Total de vendas": len(df),
        "Receita total": df["receita"].sum(),
        "Ticket médio": df["receita"].mean(),
    }


def receita_por(df, coluna):
    ## Soma a receita e agrupa por coluna ##
    return df.groupby(coluna)["receita"].sum()


def grafico_barras(serie, titulo, nome_arquivo):
    ## Gera um gráfico de barras ##
    ax = serie.plot(kind="bar", figsize=(8, 5), color="steelblue")
    ax.set_title(titulo)
    ax.set_ylabel("Receita (R$)")
    ax.set_xlabel("")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / nome_arquivo, dpi=150)
    plt.close()


def grafico_linha(serie, titulo, nome_arquivo):
    ## Gera um gráfico de linha ##
    ax = serie.plot(kind="line", marker="o", figsize=(8, 5), color="darkgreen")
    ax.set_title(titulo)
    ax.set_ylabel("Receita (R$)")
    ax.set_xlabel("Mês")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / nome_arquivo, dpi=150)
    plt.close()


def exportar_excel(metricas, por_produto, por_regiao, por_mes):
    ## Salva um relatório ##
    resumo = pd.DataFrame(list(metricas.items()), columns=["Indicador", "Valor"])
    caminho = PASTA_RELATORIOS / "relatorio_vendas.xlsx"
    with pd.ExcelWriter(caminho) as escritor:
        resumo.to_excel(escritor, sheet_name="Resumo", index=False)
        por_produto.to_excel(escritor, sheet_name="Por produto")
        por_regiao.to_excel(escritor, sheet_name="Por região")
        por_mes.to_excel(escritor, sheet_name="Por mês")
    return caminho


def main():
    if not ARQUIVO_DADOS.exists():
        print("Arquivo de dados não encontrado. Rode primeiro: python gerar_dados.py")
        return

    PASTA_GRAFICOS.mkdir(exist_ok=True)
    PASTA_RELATORIOS.mkdir(exist_ok=True)

    bruto = carregar_dados(ARQUIVO_DADOS)
    df = limpar_dados(bruto)
    print(f"Linhas antes da limpeza: {len(bruto)} | depois: {len(df)}")

    metricas = calcular_metricas(df)
    print("\n=== Indicadores ===")
    print(f"Total de vendas: {metricas['Total de vendas']}")
    print(f"Receita total:   {formatar_reais(metricas['Receita total'])}")
    print(f"Ticket médio:    {formatar_reais(metricas['Ticket médio'])}")

    por_produto = receita_por(df, "produto").sort_values(ascending=False)
    por_regiao = receita_por(df, "regiao").sort_values(ascending=False)
    por_mes = receita_por(df, "mes")

    print(f"\nProduto que mais faturou: {por_produto.idxmax()}")
    print(f"Região que mais faturou:  {por_regiao.idxmax()}")

    grafico_barras(por_produto, "Receita por produto", "receita_por_produto.png")
    grafico_barras(por_regiao, "Receita por região", "receita_por_regiao.png")
    grafico_linha(por_mes, "Evolução da receita mensal", "receita_mensal.png")

    caminho = exportar_excel(metricas, por_produto, por_regiao, por_mes)
    print(f"\nGráficos salvos em '{PASTA_GRAFICOS}' e relatório em '{caminho}'")


if __name__ == "__main__":
    main()