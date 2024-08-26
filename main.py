import pandas as pd
import os
from datetime import datetime
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
from basedados import df
from basedados import tabela_consultsie


# Criando o Dashbord no Dash
app = Dash(__name__)

server = app.server

# Criando gráficos iniciais (sem filtros aplicados)
def gerar_figura(df_filtro, y_coluna):
    fig = px.line(df_filtro, x="DataApuração", y=y_coluna, color="Apelido")
    fig.update_yaxes(range=[-5, 110]).update_layout(dragmode=False)
    return fig

#TABELA
data = tabela_consultsie[['Status', 'Porte', 'Situação', 'Dias Atraso Cobransaas', 'Data Registro', 'LT (dias)', 'Orçamento Integrado (1)', 'Obter Relatórios  (2)', 'Gerenciar Contratos Venda (3)', 
                                            'Fluxo de Caixa (4)', 'Ativação', 'Data de Ativação', 'Maturidade', '0 Uso Financeiro', 'Motivo do Risco', 'Zona de Risco', 
                                            'Engagement Score', 'Novo Engagament Score', 'Ativos x contratados', 
                                            'Financeira', 'Engenharia', 'Suprimentos', 'Comercial', 'Suporte a Decisão', 
                                            'Contábil', 'Fiscal']]
columns = [{"name": i, "id": i} for i in data.columns]


# Lista de clientes e status
lista_clientes = sorted(list(tabela_consultsie["Apelido"].unique()))
lista_clientes.append("Todos")

lista_status = sorted(list(tabela_consultsie["Status"].unique()))
lista_status.append("Todos")
print(lista_status)

# Layout corporativo
app.layout = html.Div(children=[

    #fonte Sora Medium
    html.Link(
    href="https://fonts.googleapis.com/css2?family=Sora:wght@500&display=swap",
    rel="stylesheet"
    ),
    # Cabeçalho
    html.Header(children=[
        html.Img(src='/assets/logo_sienge.png', style={"height": "90px", "margin-right": "20px", "float":"left"}),
        html.H1("Dashboard Soluções", style={"margin": "0", "padding": "20px", "color": "#ffffff"}),
    ], style={"background-color": "#181a29", "text-align": "center", "padding": "20px"}),

    # Corpo principal
    html.Div(children=[
        # Barra lateral
        html.Div(children=[
            html.H3("Filtros", style={"text-align": "center", "color": "#ffffff"}),

            # Filtro de Projetos
            html.Div(children=[
                html.Label("Status do Projeto", style={"font-size": "18px", "margin-right": "10px", "color": "#ffffff"}),
                dcc.Dropdown(options=lista_status, value=["Em andamento"], id='selecao_status',
                              style={"padding": "0px", "background-color": "#ffffff", "color": "#181a29", "border-radius": "0px"}),                               
            ], style={"padding": "20px", "background-color": "#2b2f4b", "border-radius": "10px", "margin-bottom": "30px"}),

            # Filtro de clientes
                html.Div(children=[
                html.Label("Cliente", style={"font-size": "18px", "margin-right": "10px", "color": "#ffffff"}),
                dcc.Checklist(options=lista_clientes, value=[" "], inline=False, id='selecao_clientes',
                              style={"padding": "15px", "background-color": "#2b2f4b", "border-radius": "5px"}),
            ], style={"padding": "20px", "background-color": "#2b2f4b", "border-radius": "10px", "margin-bottom": "30px"}),

        ], style={"width": "10%", "padding": "10px", "background-color": "#181a29", "color": "#ffffff", 
                  "position": "fixed", "height": "100vh", "overflow-y": "auto"}),

        # Área principal de gráficos
        html.Div(children=[
            # Subtítulo dinâmico
            html.H3(children="Clientes Consultsie", id="subtitulo", style={"padding-top": "20px"}),

            # Gráficos
            html.Div(children=[
                dcc.Graph(id='engagement_clientes', figure=gerar_figura(df, "Engagement Score")),
                dcc.Graph(id='uso_engenharia', figure=gerar_figura(df, "Engenharia")),
                dcc.Graph(id='uso_suprimentos', figure=gerar_figura(df, "Suprimentos")),
                dcc.Graph(id='uso_financeiro', figure=gerar_figura(df, "Financeira")),
                dcc.Graph(id='uso_suporte_decisão', figure=gerar_figura(df, "Suporte a Decisão")),
                dcc.Graph(id='uso_comercial', figure=gerar_figura(df, "Comercial")),
                dcc.Graph(id='uso_contabilidade', figure=gerar_figura(df, "Contábil")),
                dcc.Graph(id='uso_fiscal', figure=gerar_figura(df, "Fiscal")),
            ], style={"display": "grid", "grid-template-columns": "repeat(2, 1fr)", "gap": "20px", "padding": "20px"}),


            #TABELA
            html.Div(children=[
                dash_table.DataTable(id='table', columns=columns, data=data.to_dict('records'))
            ])

        ], style={"width": "85%", "margin-left": "15%"})  # Ajustando a margem para considerar a barra lateral
    ]),

    # Rodapé
    html.Footer(children=[
        html.P("© 2024 Time de Soluções - Todos os direitos reservados.", style={"color": "#ffffff"}),
    ], style={"background-color": "#181a29", "text-align": "center", "padding": "10px", "margin-top": "20px"}),

], style={"font-family": "Sora, sans-serif", "background-color": "#ffffff"})

# Callback para atualizar os gráficos e o subtítulo
@app.callback(
    Output('subtitulo', 'children'),
    Output('engagement_clientes', 'figure'),
    Output('uso_engenharia', 'figure'),
    Output('uso_suprimentos', 'figure'),
    Output('uso_financeiro', 'figure'),
    Output('uso_suporte_decisão', 'figure'),
    Output('uso_comercial', 'figure'),
    Output('uso_contabilidade', 'figure'),
    Output('uso_fiscal', 'figure'),
    Input('selecao_clientes', 'value')
)
def selecionar_cliente(cliente):
    if "Todos" in cliente:
        texto = "Dados de uso - Todos os clientes"
        df_filtro = df
    else:
        texto = f"Dados de uso do(s) cliente(s): {', '.join(cliente)}"
        df_filtro = df[df['Apelido'].isin(cliente)]

    # Atualizando as figuras com o filtro aplicado
    fig = gerar_figura(df_filtro, "Engagement Score")
    fig2 = gerar_figura(df_filtro, "Engenharia")
    fig3 = gerar_figura(df_filtro, "Suprimentos")
    fig4 = gerar_figura(df_filtro, "Financeira")
    fig5 = gerar_figura(df_filtro, "Suporte a Decisão")
    fig6 = gerar_figura(df_filtro, "Comercial")
    fig7 = gerar_figura(df_filtro, "Contábil")
    fig8 = gerar_figura(df_filtro, "Fiscal")

    return texto, fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8

# Colocando o seu site (seu dashboard) no ar
if __name__ == '__main__':
    #app.run_server(debug=True, host='localhost', port=8050) # http://127.0.0.1:8050/
    #app.run_server(debug=True, host='0.0.0.0')
    app.run_server(debug=True)
    

  