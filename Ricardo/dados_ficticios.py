import pandas as pd
import os

def gerar_dados():
   
    if not os.path.exists("despesas.csv"):
        dados_gastos = pd.DataFrame([
            {"Data": "01/11/2026", "Descrição": "Supermercado Pão de Açúcar", "Categoria": "Alimentação", "Valor": 450.00},
            {"Data": "02/11/2026", "Descrição": "Combustível Posto Shell", "Categoria": "Transporte", "Valor": 120.00},
            {"Data": "03/11/2026", "Descrição": "Cinema e Jantar Shopping", "Categoria": "Lazer", "Valor": 180.00},
            {"Data": "04/11/2026", "Descrição": "Conta de Luz Equatorial", "Categoria": "Moradia", "Valor": 210.00},
            {"Data": "05/11/2026", "Descrição": "Farmácia Drogasil", "Categoria": "Outros", "Valor": 65.50}
        ])
        dados_gastos.to_csv("despesas.csv", index=False)

   
    if not os.path.exists("investimentos.csv"):
        dados_inv = pd.DataFrame([
            {"Data": "01/11/2026", "Ativo/Produto": "CDB Inter 100% CDI", "Tipo": "Renda Fixa", "Valor": 500.00},
            {"Data": "03/11/2026", "Ativo/Produto": "Fundo Imobiliário MXRF11", "Tipo": "Fundos Imobiliários", "Valor": 150.00},
            {"Data": "05/11/2026", "Ativo/Produto": "Ações Petrobras (PETR4)", "Tipo": "Ações", "Valor": 300.00}
        ])
        dados_inv.to_csv("investimentos.csv", index=False)
        
