import pandas as pd
from pathlib import Path
from google.oauth2 import service_account
import pandas_gbq


pasta = Path("C:/Users/normu/Downloads/Telegram Desktop")
credentials_path = pasta / "credenciais_totvs.json"
excel_path = pasta / "dados_completos_final.xlsx"

df = pd.read_excel(excel_path)

project_id = 'seu-projeto-id'
table_id = 'entrada.tabela_final'


credentials = service_account.Credentials.from_service_account_file(str(credentials_path))

pandas_gbq.to_gbq(
    dataframe=df,
    destination_table=table_id,
    project_id=project_id,
    credentials=credentials,
    if_exists='append'
)

print("Upload de dados concluído com sucesso para '{table_id}'!")
