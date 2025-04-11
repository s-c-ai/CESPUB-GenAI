import pandas as pd
from google.oauth2 import service_account
import pandas_gbq

credentials_path = r"C:\Users\normu\Downloads\Telegram Desktop\credenciais_totvs.json"
excel_path = r"C:\Users\normu\Downloads\Telegram Desktop\dados_completos_final.xlsx"

df = pd.read_excel(excel_path)

project_id = ''
table_id = ''


credentials = service_account.Credentials.from_service_account_file(credentials_path)

pandas_gbq.to_gbq(
    dataframe=df,
    destination_table=table_id,
    project_id=project_id,
    credentials=credentials,
    if_exists='append'
)

print("Upload de dados concluído com sucesso para 'entrada.tabela_final'!")
