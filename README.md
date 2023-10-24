### Requisitos

- Ferramentas necessárias:
[Python](https://www.python.org/downloads/),
[Docker](https://www.docker.com/products/docker-desktop/),
[SQL Server Management Studio](https://learn.microsoft.com/pt-br/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16#download-ssms)


**Clonar o projeto e acessar a pasta**

```bash
$ git clone https://github.com/thoomassf/teste-delfia-rpa.git && cd teste-delfia-rpa
$ gh repo clone teste-delfia-rpa.git && cd teste-delfia-rpa
```

**Instalar contêiner do SQL Server no Docker**

```bash
$ docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<senha>" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest
```

**Criar base de dados**
```bash
$ CREATE DATABASE DB_Voos
  GO
  USE DB_Voos
  GO
  CREATE TABLE TB_Voos_SP_RIO (
    id_voo INT PRIMARY KEY IDENTITY(1,1),
      empresa VARCHAR(10),
      companhia_area VARCHAR(255),
      preco_total VARCHAR(10),
      taxa_embarque VARCHAR(10),
      taxa_servico VARCHAR(10),
      tempo_voo_min INT,
      data_hora_ida DATETIME,
      data_hora_volta DATETIME
  );
  GO
```

**Etapas para executar o script**

```bash
# Instalar dependencias do projeto
$ pip install pyodbc python-dotenv selenium datetime
# Executar 
$ python main.py
```