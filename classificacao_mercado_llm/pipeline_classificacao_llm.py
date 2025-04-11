import re
import json
import pandas as pd
from typing import TypedDict
from langgraph.graph import StateGraph, END
from google.generativeai import configure, GenerativeModel

GOOGLE_API_KEY = ""
configure(api_key=GOOGLE_API_KEY)

class MarketState(TypedDict):
    objeto: str
    descricao: str
    descricao_comp: str
    tipo: str
    cloud: str
    erp: str
    software: str
    servico: str
    saas: str
    paas: str
    iaas: str
    on_premise: str

prompt_template = """
Você é um classificador de itens de licitação pública.

Sua tarefa é analisar o conteúdo de um item (objeto, descrição e descrição complementar) e retornar SOMENTE um JSON VÁLIDO com os seguintes campos:

- "tipo": categoria geral do item (exemplos: "Serviço técnico", "Software de gestão", "Consultoria", "Infraestrutura de TI", "Material de escritório", etc.)
- "cloud": "Sim" ou "Não"
- "erp": "Sim" ou "Não"
- "software": "Sim" ou "Não"
- "servico": "Sim" ou "Não"
- "saas": "Sim" ou "Não"
- "paas": "Sim" ou "Não"
- "iaas": "Sim" ou "Não"
- "on_premise": "Sim" ou "Não"

IMPORTANTE:
- Use apenas as informações dos textos fornecidos.
- NÃO invente dados, títulos ou categorias não evidenciadas.
- NÃO escreva comentários, explicações ou qualquer conteúdo fora do JSON.

---

Exemplo 1:
Objeto: Licenciamento de sistema ERP
Descrição: Fornecimento de solução integrada para gestão administrativa
Descrição complementar: ERP com módulos de RH, compras e financeiro

Resposta esperada:
{{
  "tipo": "Software de gestão",
  "cloud": "Não",
  "erp": "Sim",
  "software": "Sim",
  "servico": "Não",
  "saas": "Não",
  "paas": "Não",
  "iaas": "Não",
  "on_premise": "Sim"
}}

---

Exemplo 2:
Objeto: Contratação de consultoria em TI
Descrição: Apoio à implementação de soluções digitais
Descrição complementar: Consultoria técnica com foco em transformação digital

Resposta esperada:
{{
  "tipo": "Consultoria",
  "cloud": "Não",
  "erp": "Não",
  "software": "Não",
  "servico": "Sim",
  "saas": "Não",
  "paas": "Não",
  "iaas": "Não",
  "on_premise": "Não"
}}

---

Exemplo 3:
Objeto: Serviço de armazenamento em nuvem
Descrição: Solução de cloud storage para backup e recuperação
Descrição complementar: Serviço baseado em SaaS com garantia de segurança

Resposta esperada:
{{
  "tipo": "Serviço de nuvem",
  "cloud": "Sim",
  "erp": "Não",
  "software": "Sim",
  "servico": "Sim",
  "saas": "Sim",
  "paas": "Não",
  "iaas": "Sim",
  "on_premise": "Não"
}}

---

Exemplo 4:
Objeto: Licença de uso de software de gestão hospitalar
Descrição: Plataforma para gerenciamento integrado de unidades de saúde
Descrição complementar: Software licenciado com funcionalidades específicas para hospitais e clínicas

Resposta esperada:
{{
  "tipo": "Software de gestão",
  "cloud": "Não",
  "erp": "Não",
  "software": "Sim",
  "servico": "Não",
  "saas": "Não",
  "paas": "Não",
  "iaas": "Não",
  "on_premise": "Sim"
}}

---

Exemplo 5:
Objeto: Contratação de serviço técnico especializado
Descrição: Manutenção preventiva e corretiva de servidores e infraestrutura de rede
Descrição complementar: Serviços técnicos recorrentes, incluindo suporte e instalação

Resposta esperada:
{{
  "tipo": "Serviço técnico",
  "cloud": "Não",
  "erp": "Não",
  "software": "Não",
  "servico": "Sim",
  "saas": "Não",
  "paas": "Não",
  "iaas": "Não",
  "on_premise": "Sim"
}}

---

Agora classifique o item abaixo com base no mesmo padrão:

Objeto: {objeto}  
Descrição: {descricao}  
Descrição complementar: {descricao_comp}
"""

def classificar_item(state: MarketState) -> MarketState:
    prompt = prompt_template.format(
        objeto=state['objeto'],
        descricao=state['descricao'],
        descricao_comp=state['descricao_comp']
    )

    model = GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    resposta_texto = response.text

    match = re.search(r"\{.*?\}", resposta_texto, re.DOTALL)

    try:
        result = json.loads(match.group()) if match else {}
        return {
            **state,
            "tipo": result.get("tipo", "Erro"),
            "cloud": result.get("cloud", "Erro"),
            "erp": result.get("erp", "Erro"),
            "software": result.get("software", "Erro"),
            "servico": result.get("servico", "Erro"),
            "saas": result.get("saas", "Erro"),
            "paas": result.get("paas", "Erro"),
            "iaas": result.get("iaas", "Erro"),
            "on_premise": result.get("on_premise", "Erro")
        }
    except Exception:
        return {
            **state,
            "tipo": "Erro",
            "cloud": "Erro",
            "erp": "Erro",
            "software": "Erro",
            "servico": "Erro",
            "saas": "Erro",
            "paas": "Erro",
            "iaas": "Erro",
            "on_premise": "Erro"
        }

workflow = StateGraph(MarketState)
workflow.add_node("classificar", classificar_item)
workflow.set_entry_point("classificar")
workflow.add_edge("classificar", END)
app = workflow.compile()

def processar_excel(input_excel, output_excel, max_rows=None):
    df = pd.read_excel(input_excel)

    if max_rows:
        df = df.head(max_rows)

    resultados = []
    for i, row in df.iterrows():
        print(f"Processando linha {i+1}/{len(df)}")

        entrada = {
            "objeto": str(row.get("objeto", "")),
            "descricao": str(row.get("descricao", "")),
            "descricao_comp": str(row.get("descricao_comp", "")),
            "tipo": "",
            "cloud": "",
            "erp": "",
            "software": "",
            "servico": "",
            "saas": "",
            "paas": "",
            "iaas": "",
            "on_premise": ""
        }

        resultado = app.invoke(entrada)
        resultados.append(resultado)

    df_resultado = pd.DataFrame(resultados)
    df_resultado.to_excel(output_excel, index=False, engine="openpyxl")
    print(f"\nResultado salvo em: {output_excel}")


if __name__ == "__main__":
    entrada = r"C:\Users\normu\Downloads\Telegram Desktop\Cópia de Estudo de Mercado V.05.03.2025 (cnpj) (1).xlsx"
    saida = "resultado_gemini_tabela_completa.xlsx"
    processar_excel(entrada, saida, max_rows=None)
