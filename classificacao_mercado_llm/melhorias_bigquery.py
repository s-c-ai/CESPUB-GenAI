import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas_gbq

credentials_path = r"C:\Users\normu\Downloads\Telegram Desktop\credenciais_totvs.json"
excel_path = r"C:\Users\normu\Downloads\Telegram Desktop\dados_completos_final.xlsx"

df = pd.read_excel(excel_path)

df.columns = df.columns.str.strip()

if 'tipo_cliente_totvs' in df.columns:
    df['tipo_cliente_totvs'] = df['tipo_cliente_totvs'].astype(str).str.strip()
    df['tipo_cliente_totvs'] = df['tipo_cliente_totvs'].replace({'': 'não informado', 'nan': 'não informado'})

project_id = 'totvs-cespub'
table_id = 'entrada.tabela_final_atualizada'
credentials = service_account.Credentials.from_service_account_file(credentials_path)
client = bigquery.Client(project=project_id, credentials=credentials)

table = client.get_table(f"{project_id}.{table_id}")
existing_columns = [field.name for field in table.schema]
df = df[[col for col in df.columns if col in existing_columns]]

pandas_gbq.to_gbq(
    dataframe=df,
    destination_table=table_id,
    project_id=project_id,
    credentials=credentials,
    if_exists='append'
)

print("Upload concluído com sucesso!")
