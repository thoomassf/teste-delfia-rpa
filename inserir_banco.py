import pyodbc
from dotenv import load_dotenv
import os

def inserir_voos_bd(dados):
    # Carregue as variáveis de ambiente do arquivo .env
    load_dotenv()
    # Acesse as variáveis de ambiente
    server = os.getenv("SERVER")
    database = os.getenv("DATABASE")
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")
    
    # Crie uma conexão pyodbc
    conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}")

    # Crie um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Insira os dados na tabela
    for i in range(len(dados['empresa'])):
        cursor.execute("""
            INSERT INTO TB_Voos_SP_RIO (empresa, companhia_area, preco_total, taxa_embarque, taxa_servico, tempo_voo_min, data_hora_ida, data_hora_volta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        dados['empresa'][i], dados['companhia_area'][i], dados['preco_total'][i],
        dados['taxa_embarque'][i], dados['taxa_servico'][i], dados['tempo_voo_min'][i],
        dados['data_hora_ida'][i], dados['data_hora_volta'][i])

    # Comite as alterações
    conn.commit()

    # Feche o cursor e a conexão
    cursor.close()
    conn.close()

# #Testar função
# Dicionário com os dados
# dic_voos = {
#     'empresa': ['Empresa1', 'Empresa2'],
#     'companhia_area': ['Companhia1', 'Companhia2'],
#     'preco_total': ['100.00', '150.00'],
#     'taxa_embarque': ['10.00', '12.00'],
#     'taxa_servico': ['5.00', '6.00'],
#     'tempo_voo_min': [120, 180],
#     'data_hora_ida': ['01/11/23 12:00', '01/11/23 12:00'],
#     'data_hora_volta': ['04/11/23 16:00', '04/11/23 16:00']
# }

# inserir_voos_bd(dic_voos)