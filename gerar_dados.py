import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(42)

PRODUTOS = {
    "Camiseta": 49.90,
    "Calça Jeans": 139.90,
    "Tênis": 249.90,
    "Boné": 39.90,
    "Jaqueta": 299.90,
    "Meia": 14.90,
}
REGIOES = ["Sul", "Sudeste", "Nordeste", "Norte", "Centro-Oeste"]


def gerar_vendas(quantidade=1000):
    ## Cria uma tabela de vendas com vendas fictícias ##
    inicio = date(2025, 1, 1)
    linhas = []
    for _ in range(quantidade):
        produto = random.choice(list(PRODUTOS))
        linhas.append({
            "data": inicio + timedelta(days=random.randint(0, 364)),
            "produto": produto,
            "regiao": random.choice(REGIOES),
            "quantidade": random.randint(1, 5),
            "preco_unitario": PRODUTOS[produto],
        })
    return pd.DataFrame(linhas)


def sujar_dados(df):
    ## Insere problemas comuns de dados reais: campos vazios e duplicatas ##
    indices_vazios = df.sample(15, random_state=1).index
    df.loc[indices_vazios, "regiao"] = None
    duplicadas = df.sample(10, random_state=2)
    return pd.concat([df, duplicadas], ignore_index=True)


if __name__ == "__main__":
    Path("dados").mkdir(exist_ok=True)
    vendas = sujar_dados(gerar_vendas())
    vendas.to_csv("dados/vendas.csv", index=False)
    print(f"Arquivo criado com {len(vendas)} linhas em dados/vendas.csv")





