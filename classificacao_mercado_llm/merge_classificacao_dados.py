import pandas as pd

original = pd.read_excel(r"C:\Users\normu\Downloads\Telegram Desktop\Cópia de Estudo de Mercado V.05.03.2025 (cnpj) - Copia.xlsx")
classificada = pd.read_excel(r"C:\Users\normu\Downloads\Telegram Desktop\resultado_gemini_tabela_completa.xlsx")

assert len(original) == len(classificada)

original["valor_total"] = (
    original["valor_total"]
    .astype(str)
    .str.replace("R$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

original["valor_total"] = original["valor_total"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

dados_completos = pd.concat([original, classificada.drop(columns=['objeto', 'descricao', 'descricao_comp'])], axis=1)

dados_completos.to_excel("dados_completos_final.xlsx", index=False)
print("Arquivo 'dados_completos_final.xlsx' gerado com sucesso.")
