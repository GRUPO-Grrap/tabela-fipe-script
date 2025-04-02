import os
import pandas as pd
import re
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv

load_dotenv()

arquivo_csv = "./data/tabela-fipe-historico-precos.csv"

# Função para limpar números, removendo pontos e outros caracteres
def limpar_numeros(valor):
    if isinstance(valor, str):
        return re.sub(r'\D', '', valor)
    return valor

if os.path.exists(arquivo_csv):
    encodings = ["utf-8"]
    for enc in encodings:
        try:
            tabela_fipe = pd.read_csv(arquivo_csv, encoding=enc)
            print(f"Dados carregados com sucesso usando encoding: {enc}")
            break
        except UnicodeDecodeError:
            print(f"Erro ao carregar com encoding: {enc}, tentando outro...")
    
    print("Colunas encontradas:", tabela_fipe.columns)
    print(tabela_fipe.head(n = 10))

    columns = ('codigoFipe', 'marca', 'modelo', 'anoModelo', 'mesReferencia', 'anoReferencia', 'valor')

    if not all(col in tabela_fipe.columns for col in columns):
        print("Erro: Algumas colunas não estão presentes no arquivo!")

    # Remover duplicatas
    tabela_fipe.drop_duplicates(inplace=True)  
    tabela_fipe.columns = [col.lower().replace(" ", "_") for col in tabela_fipe.columns]

    # Remover caracteres não numéricos apenas das colunas numéricas
    for col in tabela_fipe.select_dtypes(include=['object']).columns:
        if tabela_fipe[col].str.replace(" ", "").str.isnumeric().all():
            tabela_fipe[col] = tabela_fipe[col].apply(limpar_numeros)
    
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port")
    database = os.getenv("database")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    metadata = MetaData()

    metadata.reflect(bind=engine)
    tabela_fipe_db_metadata = metadata.tables.get(os.getenv("table_name"))

    if tabela_fipe_db_metadata is not None:
        with engine.begin() as conn:
            result = conn.execute(tabela_fipe_db_metadata.select().limit(1))
            if result.fetchall():
                conn.execute(tabela_fipe_db_metadata.delete())
                print("Dados deletados no PostgreSQL com sucesso!")
            else:
                print("A tabela já está vazia")

    tabela_fipe.to_sql(database, engine, if_exists="append", index=False)
    print("Dados inseridos no PostgreSQL com sucesso!")
    print(pd.read_sql(f'SELECT * FROM {os.getenv("table_name")} LIMIT 2', con=engine))

else:
    print(f"Arquivo não encontrado: {arquivo_csv}")
