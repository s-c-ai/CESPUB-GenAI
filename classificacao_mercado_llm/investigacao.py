import pandas as pd

excel_path = r"C:\Users\normu\Downloads\Telegram Desktop\dados_completos_final.xlsx"

df = pd.read_excel(excel_path)

print("Nome das colunas no Excel:")
print(df.columns.tolist())

possiveis_nomes = [col for col in df.columns if "totvs" in col.lower()]
print("\n Possíveis colunas que se referem a cliente TOTVS:")
print(possiveis_nomes)

for nome in possiveis_nomes:
    print(f"\nConteúdo de '{nome}':")
    print(df[nome].head(10))
