import pandas as pd
import os
from datetime import datetime
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px

#Leitura dos arquivos: Sensedata e Controle de Projetos
tabela_sensedata = pd.read_csv(r'sensedata.csv', sep='|', low_memory=False) # importa o arquivo em excel 
tabela_consultsie = pd.read_excel(r'projetos_consultsie.xlsx')
#tabela_sensedata.info() #Exibe dados do arquivo
#tabela_consultsie.info() #Exibe dados do arquivo
# tabela_df = tabela_df.dropna(how="all", axis=0) # limpar linhas (axis 0) vazias Nan
# tabela_df = tabela_df.dropna(how="all", axis=1) # limpar colunas (axis 1) vazias Nan

#tabela_sensedata = tabela_sensedata.drop([], axis=1) # para retirar colunas utiliza o método 'drop'.
tabela_sensedata_format = tabela_sensedata[['Cliente', 'Sense Score', 'MRR', 'Situação', 'Dias Atraso Cobransaas', 'Data Registro', 'CNPJ', 'Porte', 'Porte Mercado', 'CSM', 'Sponsor', 'E-mail Sponsor', 'Telefone Sponsor', 'Cidade', 'Estado', 'Usuários Ativos', 'LT (meses)', 'LT (dias)', 'Estágio Ideal do Onboarding', 'Estágio Conquistado do Onboarding', 'Orçamento Integrado (1)', 'Obter Relatórios  (2)', 'Gerenciar Contratos Venda (3)', 'Fluxo de Caixa (4)', 'Ativação', 'Data de Ativação', 'Data limite para atv e onb', 'Maturidade', '0 Uso Financeiro', 'Motivo do Risco', 'Zona de Risco', 'Engagement Score', 'Novo Engagament Score', 'Ativos x contratados', 'Financeira', 'Engenharia', 'Suprimentos', 'Comercial', 'Suporte a Decisão', 'Contábil', 'Fiscal', 'Usa Orçamento', 'Usa Planejamento', 'Usa Acompanhamento', 'Usa Compras', 'Usa Contratos e Medições', 'Usa Conciliação', 'Usa Vendas', 'Usa Gerencial de Financeiro', 'Usa Gerencial de Obras', 'Usa Gerencial Obras Avançado', 'Usa Gerencial de Suprimentos', 'Usa Orçamento Empresarial', 'Usa Integração Contábil', 'Usa Contabilidade', 'Usa Obrigações Fiscais' ,  'Sistema']] # para escolher as colunas para indicar dentro dos []

#display(tabela_sensedata_format)

tabela_consultsie = tabela_consultsie.merge(tabela_sensedata_format, on='Cliente', suffixes=(None, None))
tabela_consultsie['DataApuração'] = datetime.now().strftime('%d/%m/%Y')


#Criar um nome de arquivo com data e hora atual
agora = datetime.now().strftime('%Y%m%d_%H%M%S')
tabela_consultsie.to_excel('Resultados_excel/tabela_consultsie_{}.xlsx'.format(agora))
print("Arquivo Excel salvo com sucesso.")

# tabela_consultsie.info()

#Consolidar a leitura do arquivo atual + arquivos anteriores
path = 'Resultados_excel'
files = os.listdir(path)
df = pd.DataFrame()
#print(files)

#Agrupar os dados de todos os arquivos em um único DataFrame
files_xlsx = [path + '/' + f for f in files if f[-4:] == 'xlsx']
for f in files_xlsx:
    data = pd.read_excel(f)
    df = pd.concat([df, data])
#display(df)

df.to_excel('tabela_consolidada.xlsx')

#Convertendo datas
df["DataProjeto"] = pd.to_datetime(df.DataProjeto)
df["DataProjeto"] = df["DataProjeto"].dt.strftime('%d/%m/%Y')
df["DataApuração"] = pd.to_datetime(df.DataApuração)
df["DataApuração"] = df["DataApuração"].dt.strftime('%d/%m/%Y')

# # Aplicando Filtros
# clientes_risco = tabela_consultsie[tabela_consultsie['Situação'] == 'Risco']
# clientes_atrasosaas = tabela_consultsie[tabela_consultsie['Dias Atraso Cobransaas'] > 0]
# clientes_comercial = df[df['Sistema'].str.contains("VENDAS")]
# clientes_contabilidade = df[df['Sistema'].str.contains("INTEGRAÇÃO CONTÁBIL", "CONTABILIDADE")]
# clientes_engenharia = df[df['Sistema'].str.contains("ORÇAMENTO")]
# clientes_fiscal = df[df['Sistema'].str.contains("OBRIGAÇÕES FISCAIS")]

# display(clientes_risco)
# display(clientes_atrasosaas)
# display(clientes_comercial)
# display(clientes_contabilidade)
# display(clientes_engenharia)
# display(clientes_fiscal)