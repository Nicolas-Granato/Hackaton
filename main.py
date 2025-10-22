#depois eu encaixo o banco de dados
import os
from sqlalchemy import create_engine, text
from langchain_community.agent_toolkits import SQLDatabaseToolkit 
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase


