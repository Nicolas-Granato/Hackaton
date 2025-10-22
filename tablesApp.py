import pandas as pd
from sqlalchemy import create_engine
import os
import streamlit as st

DB_PATH = "banco_de_dados_provisorio.db"

CSV_BOVINOS = "dados\\bovinos.csv"
CSV_LACTACAO = "dados\\fichalactacao.csv"
CSV_OCORRENCIA_EVENTO = "dados\\ocorrenciaEvento.csv"   #organizacao arquivos .csv usados
CSV_EVENTOS = "dados\\eventos.csv"


TBL_BOVINOS = "Bovinos"
TBL_ASSOCIACAO_BOVINOS = "Associacao pai/mae --> filho"
TBL_OCORRENCIA_EVENTOS = "Evento"                       #organizacao das futuras tabelas
TBL_FICHA_LACTACAO = "Ficha Lactacao"
TBL_TIPO_EVENTO = "Tipos de evento"

@st.cache_resource
def setupdatabase():

    if os.path.exists(DB_PATH): #verificando se já existe o banco de dados, caso não exista, vai criar um
        print("Cache: Banco de dados normalizado já encontrado.")
        return

    print("Iniciando ETL: Lendo CSV bruto.") #Extract, Transform, Load

    try: 
        df_bruto_bovinos = pd.read_csv(CSV_BOVINOS)
        df_bruto_lactacao = pd.read_csv(CSV_LACTACAO)
        df_bruto_eventos = pd.read_csv(CSV_EVENTOS)
        df_bruto_ocorrencia_eventos = pd.read_csv(CSV_OCORRENCIA_EVENTO)
    
    except FileNotFoundError:   #verificando a existencia dos arquivos csv

        if FileNotFoundError(CSV_BOVINOS):
            print(f"ERRO: Arquivo {CSV_BOVINOS} não encontrado")
        
        if FileNotFoundError(CSV_EVENTOS):
            print(f"ERRO: Arquivo {CSV_EVENTOS} não encontrado")

        if FileNotFoundError(CSV_LACTACAO):
            print(f"ERRO: Arquivo {CSV_LACTACAO} não encontrado")
        
        if FileNotFoundError(CSV_OCORRENCIA_EVENTO):
            print(f"ERRO: Arquivo {CSV_OCORRENCIA_EVENTO} não encontrado")
    
    print("Normalizando tabelas...")

    df_dim_bovinos = df_bruto_bovinos[["codigo","nome","sexo","pais_origem","raca","data_nascimento"]].drop_duplicates #criando os dataframes
    df_dim_associacao_bovinos = df_bruto_bovinos[["codigo","numerorgpai","numerorgmae"]].drop_duplicates

    df_dim_tipo_evento = df_bruto_eventos[["id_evento","evento"]].drop_duplicates   
    df_dim_ocorrencia_evento = df_bruto_ocorrencia_eventos[["codigo_bovino","dataocorrencia","tipo_evento"]].drop_duplicates
    
    df_dim_ficha_lactacao = df_bruto_ocorrencia_eventos[["codigo_bovino","formacoleta","idademesesparto","numeroordenhas","quantidadediaslactacao","qtdeleite305","qtdegordura305","qtdeproteina305","dataencerramento","ideventoparto","ideventoseca"]].drop_duplicates

    df_dim_associacao_bovinos = df_dim_associacao_bovinos.reset_index() #adicionando Primary Keys
    df_dim_associacao_bovinos = df_dim_associacao_bovinos.rename(columns={"index","associacao_id"})
    df_dim_associacao_bovinos["associacao_id"] = "ab_" + df_dim_associacao_bovinos["associacao_id"].astype(str)

    df_dim_ficha_lactacao = df_dim_ficha_lactacao.reset_inde()
    df_dim_ficha_lactacao = df_dim_ficha_lactacao.rename(columns={"index","ficha_id"})
    df_dim_ficha_lactacao["ficha_id"] = "fl_" + df_dim_ficha_lactacao["ficha_id"].astype(str)

    df_bruto_ocorrencia_eventos = df_bruto_ocorrencia_eventos.reset_index()
    df_bruto_ocorrencia_eventos = df_bruto_ocorrencia_eventos.rename(columns={"index","ocorrencias_id"})
    df_bruto_ocorrencia_eventos["ocorrencias_id"] = "oe_" + df_bruto_ocorrencia_eventos["ocorrencias_id"].astype(str)

