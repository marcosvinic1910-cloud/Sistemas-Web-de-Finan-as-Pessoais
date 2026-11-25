import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os


from dados_ficticios import gerar_dados
gerar_dados()



st.set_page_config(layout="wide")

with open("eduarda.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.markdown("""
<div class="banner-topo">
    <h1>💳 Sistema Web de Finanças Pessoais</h1>
    <p>Rastreador Inteligente de Gastos, Investimentos e Benefícios</p>
</div>
""", unsafe_allow_html=True)



st.sidebar.header("⚙️ Configurações")
orcamento = st.sidebar.number_input("Orçamento Mensal (R$)", value=2000.0)
vale_alimentacao = st.sidebar.number_input("Vale Alimentação (R$)", value=600.0)
vale_transporte = st.sidebar.number_input("Vale Transporte (R$)", value=250.0)



if os.path.exists("despesas.csv"):
    df_gastos = pd.read_csv("despesas.csv")
else:
    df_gastos = pd.DataFrame(columns=["Data", "Descrição", "Categoria", "Valor"])

if os.path.exists("investimentos.csv"):
    df_investimentos = pd.read_csv("investimentos.csv")
else:
    df_investimentos = pd.DataFrame(columns=["Data", "Ativo/Produto", "Tipo", "Valor"])


total_gasto = df_gastos["Valor"].sum()
total_investido = df_investimentos["Valor"].sum()
saldo_restante = orcamento - total_gasto



gasto_alimentacao = df_gastos[df_gastos["Categoria"] == "Alimentação"]["Valor"].sum()
saldo_va = vale_alimentacao - gasto_alimentacao

gasto_transporte = df_gastos[df_gastos["Categoria"] == "Transporte"]["Valor"].sum()
saldo_vt = vale_transporte - gasto_transporte

st.markdown("---")


col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(label="💰 Orçamento", value=f"R$ {orcamento:,.2f}")

with col2:
    st.metric(label="📉 Total Gasto", value=f"R$ {total_gasto:,.2f}")

with col3:
    st.metric(label="🐷 Investido", value=f"R$ {total_investido:,.2f}")

with col4:
    cor_saldo = "normal" if saldo_restante >= 0 else "inverse"
    st.metric(label="🏪 Saldo Livre", value=f"R$ {saldo_restante:,.2f}", delta=f"R$ {saldo_restante:,.2f}", delta_color=cor_saldo)

with col5:
    st.metric(label="🍽️ Vale Alimentação", value=f"R$ {saldo_va:,.2f}", delta=f"Total: R$ {vale_alimentacao:,.2f}", delta_color="off")

with col6:
    st.metric(label="🚌 Vale Transporte", value=f"R$ {saldo_vt:,.2f}", delta=f"Total: R$ {vale_transporte:,.2f}", delta_color="off")



if total_gasto > orcamento:
    st.error("🚨 **ALERTA MÁXIMO:** Você estourou seu orçamento de gastos!")
elif total_gasto >= orcamento * 0.8:
    st.warning("⚠️ **ATENÇÃO:** Você já usou mais de 80% do seu orçamento de gastos!")

st.markdown("---")


aba_gastos, aba_investimentos = st.tabs(["🛒 Controle de Gastos", "📈 Meus Investimentos"])



with aba_gastos:
    st.write("### 📝 Registrar Nova Despesa")
    col_form1, col_form2 = st.columns(2)

    with col_form1:
        descricao_gasto = st.text_input("Descrição do Gasto (ex: Mercado, Gasolina)")
        categoria_gasto = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Moradia", "Outros"])

    with col_form2:
        valor_gasto = st.number_input("Valor da Despesa (R$)", min_value=0.0, key="v_gasto")
        data_gasto = st.date_input("Data do Gasto", value=datetime.now().date(), key="d_gasto")

    if st.button("Salvar Gasto"):
        if descricao_gasto != "" and valor_gasto > 0:
            novo_gasto = pd.DataFrame([{
                "Data": data_gasto.strftime("%d/%m/%Y"),
                "Descrição": descricao_gasto,
                "Categoria": categoria_gasto,
                "Valor": valor_gasto
            }])
            df_gastos = pd.concat([df_gastos, novo_gasto], ignore_index=True)
            df_gastos.to_csv("despesas.csv", index=False)
            st.success("Gasto registrado com sucesso!")
            st.rerun()
        else:
            st.error("Preencha a descrição e coloque um valor maior que zero.")

    st.markdown("---")
    st.write("### 📋 Histórico Geral de Despesas")
    st.dataframe(df_gastos, width="stretch")

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.download_button(
            label="📥 Baixar Planilha de Gastos (CSV)",
            data=df_gastos.to_csv(index=False).encode("utf-8"),
            file_name="meus_gastos.csv",
            mime="text/csv"
        )
    with col_b2:
        if st.button("🗑️ Apagar Último Gasto"):
            if not df_gastos.empty:
                df_gastos = df_gastos.iloc[:-1]
                df_gastos.to_csv("despesas.csv", index=False)
                st.rerun()

    if not df_gastos.empty:
        st.markdown("---")
        st.write("### 📊 Distribuição de Gastos por Categoria")
        grafico_gastos = px.pie(
            df_gastos, 
            values="Valor", 
            names="Categoria", 
            title="Para onde está indo o seu dinheiro?",
            hole=0.4
        )
        st.plotly_chart(grafico_gastos, width="stretch")



with aba_investimentos:
    st.write("### 📝 Registrar Novo Investimento")
    col_inv1, col_inv2 = st.columns(2)

    with col_inv1:
        ativo_investido = st.text_input("Nome do Investimento (ex: Tesouro Direto, CDB Itaú, Ação X)")
        tipo_investimento = st.selectbox("Tipo de Ativo", ["Renda Fixa", "Ações", "Fundos Imobiliários", "Criptomoedas", "Outros"])

    with col_inv2:
        valor_investido = st.number_input("Valor Investido (R$)", min_value=0.0, key="v_inv")
        data_investido = st.date_input("Data do Investimento", value=datetime.now().date(), key="d_inv")

    if st.button("Salvar Investimento"):
        if ativo_investido != "" and valor_investido > 0:
            novo_investimento = pd.DataFrame([{
                "Data": data_investido.strftime("%d/%m/%Y"),
                "Ativo/Produto": ativo_investido,
                "Tipo": tipo_investimento,
                "Valor": valor_investido
            }])
            df_investimentos = pd.concat([df_investimentos, novo_investimento], ignore_index=True)
            df_investimentos.to_csv("investimentos.csv", index=False)
            st.success("Investimento registrado com sucesso!")
            st.rerun()
        else:
            st.error("Preencha o nome do investimento e coloque um valor maior que zero.")

    st.markdown("---")
    st.write("### 📋 Histórico Geral de Investimentos")
    st.dataframe(df_investimentos, width="stretch")

    col_inv_b1, col_inv_b2 = st.columns(2)
    with col_inv_b1:
        st.download_button(
            label="📥 Baixar Planilha de Investimentos (CSV)",
            data=df_investimentos.to_csv(index=False).encode("utf-8"),
            file_name="meus_investimentos.csv",
            mime="text/csv"
        )
    with col_inv_b2:
        if st.button("🗑️ Apagar Último Investimento"):
            if not df_investimentos.empty:
                df_investimentos = df_investimentos.iloc[:-1]
                df_investimentos.to_csv("investimentos.csv", index=False)
                st.rerun()

    if not df_investimentos.empty:
        st.markdown("---")
        st.write("### 📊 Meus Investimentos por Tipo")
        grafico_inv = px.bar(
            df_investimentos, 
            x="Tipo", 
            y="Valor", 
            color="Tipo",
            title="Total acumulado por tipo de ativo"
        )
        st.plotly_chart(grafico_inv, width="stretch")

        
