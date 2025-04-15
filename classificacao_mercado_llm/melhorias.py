import pandas as pd

caminho_entrada = r"C:\Users\normu\Downloads\Telegram Desktop\dados_completos_final.xlsx"

caminho_saida = r"C:\Users\normu\Downloads\dados_completos_com_padronizacao.xlsx"

df = pd.read_excel(caminho_entrada)

def combinar_modelos_cloud(row):
    modelos = []
    if row['saas'] == 'Sim':
        modelos.append('SaaS')
    if row['paas'] == 'Sim':
        modelos.append('PaaS')
    if row['iaas'] == 'Sim':
        modelos.append('IaaS')
    if row['on_premise'] == 'Sim':
        modelos.append('On-Premise')
    return ', '.join(modelos) if modelos else 'Nenhum'

df['modelos_cloud'] = df.apply(combinar_modelos_cloud, axis=1)

def padronizar_razao_social(nome):
    nome = str(nome).upper().strip()

    # TOTVS
    if nome in ['TOTVS', 'TOTVS S.A.', 'TOTVS SA', 'TOTVS S/A']:
        return 'TOTVS'
    elif 'TOTVS' in nome:
        return 'TOTVS'

    # SPASSU
    if nome in ['SPASSU TECNOLOGIA E SERVICOS S. A', 'SPASSU TECNOLOGIA E SERVIÇOS S.A.', 'SPASSU TECNOLOGIA']:
        return 'SPASSU'
    elif 'SPASSU' in nome:
        return 'SPASSU'

    # ENGINE
    if nome in ['ENGINE BR TECNOLOGIA LTDA', 'ENGINE TECNOLOGIA']:
        return 'ENGINE'
    elif 'ENGINE' in nome:
        return 'ENGINE'

    # IPQ TECNOLOGIA
    if nome in ['IPQ TECNOLOGIA LTDA', 'IPQ TECNOLOGIA E SERVICOS']:
        return 'IPQ TECNOLOGIA'
    elif 'IPQ' in nome:
        return 'IPQ TECNOLOGIA'

    # TELETEX
    if nome in ['TELETEX COMPUTADORES E SISTEMAS LTDA', 'TELETEX SISTEMAS']:
        return 'TELETEX'
    elif 'TELETEX' in nome:
        return 'TELETEX'

    # CONSÓRCIO
    if nome in ['CONSÓRCIO TRANSFORMAÇÃO DIGITAL', 'CONSORCIO TRANSFORMACAO DIGITAL']:
        return 'CONSÓRCIO'
    elif 'CONSÓRCIO' in nome or 'CONSORCIO' in nome:
        return 'CONSÓRCIO'

    return nome.split()[0]


df['razao_social_padronizada'] = df['razao_social'].apply(padronizar_razao_social)

variacoes_empresas = (
    df.groupby('razao_social_padronizada')['razao_social']
    .nunique()
    .reset_index(name='variacoes')
)

print(df[['razao_social', 'razao_social_padronizada', 'modelos_cloud']].head())
print("\nVariações por empresa padronizada:")
print(variacoes_empresas.sort_values(by='variacoes', ascending=False))

df.to_excel(caminho_saida, index=False)
print(f"\n Arquivo salvo com sucesso em: {caminho_saida}")
