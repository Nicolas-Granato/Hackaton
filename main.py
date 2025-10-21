import pandas as pd
from sqlalchemy import create_engine
import os
import streamlit as st

DB_PATH = "banco_de_dados_provisorio.db"

CSV_BOVINOS = "dados\\bovinos.csv"
CSV_LACTACAO = "dados\\fichalactacao.csv"
CSV_EVENTO = "dados\\ocorrenciaEvento.csv"

TBL_BOVINOS = "Bovinos"
TBL_ASSOCIACAO_BOVINOS = "Associacao pai/mae --> filho"
TBL_OCORRENCIA_EVENTOS = "Evento"
TBL_FICHA_LACTACAO = "Ficha Lactacao"

TBL_TIPO_ASSOCIACAO = "Mae ou pai"
TBL_TIPO_EVENTO = "Tipos de evento"

@st.cache_resource
def setupdatabase():

    if os.path.exists(DB_PATH):
        print("Cache: Banco de dados normalizado já encontrado.")
        return

    print("Iniciando ETL: Lendo CSV bruto.")

    try: 
        df_bruto_bovinos = pd.read_csv(CSV_BOVINOS)
        df_bruto_lactacao = pd.read_csv(CSV_LACTACAO)
        df_bruto_evento = pd.read_csv(CSV_EVENTO)
    
    except FileNotFoundError:

        if FileNotFoundError(CSV_BOVINOS):
            print(f"ERRO: Arquivo {CSV_BOVINOS} não encontrado")
        
        if FileNotFoundError(CSV_EVENTO):
            print(f"ERRO: Arquivo {CSV_EVENTO} não encontrado")

        if FileNotFoundError(CSV_LACTACAO):
            print(f"ERRO: Arquivo {CSV_LACTACAO} não encontrado")
    
    print("Normalizando tabelas...")

    df_dim_bovinos = df_bruto_bovinos[["codigo","nome","sexo","pais_origem","raca","data_nascimento"]].drop_duplicates

    df_dim_associacao_bovinos = 

