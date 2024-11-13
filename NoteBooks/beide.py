# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # Zet de titel en layout van de app
# st.set_page_config(page_title="Bedrijven Inkoop Analyse", layout="wide")

# # Functie om de data in te laden en voor te bereiden
# @st.cache_data
# def load_data():
#     df = pd.read_csv('NoteBooks/Data/inkoop.csv')
#     df['Datum'] = pd.to_datetime(df['Datum'], format="%d/%m/%Y", errors='coerce')
#     df['Jaar'] = df['Datum'].dt.year
#     df['Totaal gespendeerd'] = df['Totaal gespendeerd'].replace({'€': '', ',': ''}, regex=True).astype(float)
#     return df

# # Laad de data
# df = load_data()


# # Sidebar-menu voor navigatie tussen pagina's
# st.sidebar.title("Navigatie")
# pagina = st.sidebar.radio("Ga naar", ["Home 🏠", "Inkoop 💸"])

# # Home-pagina met uitleg
# if pagina == "Home 🏠":
#     st.title("Bedrijven Inkoop Analyse")
#     st.write("""
#     Welkom bij de Bedrijven Inkoop Analyse App. Deze applicatie toont een overzicht van de totale bestedingen 
#     per bedrijf over meerdere jaren, met de mogelijkheid om gegevens voor specifieke jaren en bedrijven te selecteren.
    
#     Gebruik het menu aan de zijkant om te navigeren tussen de verschillende pagina's.
#     """)

# # Inkoop-pagina met grafieken
# elif pagina == "Inkoop 💸":
#     st.title("Inkoop Overzicht per Bedrijf")
    
#     # Filteropties: selecteer jaar en bedrijf
#     jaren_selectie = st.multiselect("Selecteer jaar", options=df['Jaar'].unique(), default=df['Jaar'].unique())
#     bedrijven_selectie = st.multiselect("Selecteer bedrijven", options=df['Company'].unique(), default=df['Company'].unique())
    
#     # Filter de data op basis van de selectie
#     gefilterde_data = df[(df['Jaar'].isin(jaren_selectie)) & (df['Company'].isin(bedrijven_selectie))]
    
#     # Groepeer de gefilterde data per bedrijf en jaar en bereken de totaalbedragen
#     totaal_per_bedrijf_jaar = gefilterde_data.groupby(['Company', 'Jaar'])['Totaal gespendeerd'].sum().reset_index()
    
#     # Maak de interactieve Plotly-grafiek
#     fig = px.bar(
#         totaal_per_bedrijf_jaar,
#         x='Company', 
#         y='Totaal gespendeerd', 
#         color='Jaar',
#         title="Totaal Bedrag per Bedrijf per Jaar",
#         labels={'Totaal gespendeerd': 'Totaal gespendeerd (€)', 'Company': 'Bedrijf'}
#     )
    
#     # Toon de grafiek in de app
#     st.plotly_chart(fig, use_container_width=True)

#     # Extra uitleg of data weergeven
#     st.write("De grafiek hierboven toont de totale uitgaven per bedrijf voor de geselecteerde jaren.")
#########################
# import pandas as pd
# import plotly.express as px
# from dash import Dash, dcc, html
# from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc

# # Laad de data in en bereid deze voor
# def load_data():
#     df = pd.read_csv('NoteBooks/Data/inkoop.csv')
#     df['Datum'] = pd.to_datetime(df['Datum'], format="%d/%m/%Y", errors='coerce')
#     df['Jaar'] = df['Datum'].dt.year
#     df['Totaal gespendeerd'] = df['Totaal gespendeerd'].replace({'€': '', ',': ''}, regex=True).astype(float)
#     return df

# # Data inladen
# df = load_data()

# # Initialiseer de Dash-applicatie met Bootstrap stijl
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.title = "Bedrijven Inkoop Analyse"

# # Layout met sidebar en content
# app.layout = dbc.Row([
#     # Sidebar aan de linkerzijde
#     dbc.Col([
#         html.H2("Navigatie", style={'textAlign': 'center', 'color': 'white'}),
#         dcc.RadioItems(
#             id='pagina-keuze',
#             options=[
#                 {'label': 'Home 🏠', 'value': 'home'},
#                 {'label': 'Inkoop 💸', 'value': 'inkoop'}
#             ],
#             value='home',
#             labelStyle={'display': 'block', 'padding': '10px', 'fontSize': '18px'},
#             style={'backgroundColor': '#343a40', 'color': 'white'}
#         ),
#     ], width=3, style={'backgroundColor': '#343a40', 'height': '100vh'}),  # Sidebar kleur

#     # Hoofdcontent aan de rechterzijde
#     dbc.Col([
#         html.Div(id='pagina-content')
#     ], width=9)
# ])

# # Callback voor dynamische pagina-inhoud
# @app.callback(
#     Output('pagina-content', 'children'),
#     Input('pagina-keuze', 'value')
# )
# def display_page(pagina):
#     if pagina == 'home':
#         return html.Div([
#             html.H1("Welkom bij de Bedrijven Inkoop Analyse", style={'textAlign': 'center'}),
#             html.P("""
#                 Deze applicatie toont een overzicht van de totale bestedingen per bedrijf over meerdere jaren,
#                 met de mogelijkheid om gegevens voor specifieke jaren en bedrijven te selecteren.
#                 Gebruik de navigatie aan de zijkant om tussen de verschillende pagina's te schakelen.
#             """, style={'textAlign': 'center'})
#         ])
#     elif pagina == 'inkoop':
#         return html.Div([
#             html.H1("Inkoop Overzicht per Bedrijf", style={'textAlign': 'center'}),
#             html.Div([
#                 html.Label('Selecteer jaar:'),
#                 dcc.Dropdown(
#                     id='jaar-dropdown',
#                     options=[{'label': str(jaar), 'value': jaar} for jaar in sorted(df['Jaar'].unique())],
#                     multi=True,
#                     value=df['Jaar'].unique(),  # Standaard alle jaren geselecteerd
#                     placeholder='Selecteer jaar'
#                 ),
#                 html.Label('Selecteer bedrijven:'),
#                 dcc.Dropdown(
#                     id='bedrijf-dropdown',
#                     options=[{'label': bedrijf, 'value': bedrijf} for bedrijf in sorted(df['Company'].unique())],
#                     multi=True,
#                     value=df['Company'].unique(),  # Standaard alle bedrijven geselecteerd
#                     placeholder='Selecteer bedrijf'
#                 )
#             ], style={'width': '40%', 'padding': '20px', 'margin': 'auto'}),
#             html.Div([
#                 dcc.Graph(id='inkoop-graph')
#             ], style={'padding': '20px'}),
#         ])

# # Callback voor de grafiek update op basis van de dropdown keuzes
# @app.callback(
#     Output('inkoop-graph', 'figure'),
#     [Input('jaar-dropdown', 'value'),
#      Input('bedrijf-dropdown', 'value')]
# )
# def update_graph(selected_years, selected_companies):
#     # Filter de data op basis van selectie
#     filtered_data = df[(df['Jaar'].isin(selected_years)) & (df['Company'].isin(selected_companies))]

#     # Groepeer de gefilterde data per bedrijf en jaar en bereken de totaalbedragen
#     totaal_per_bedrijf_jaar = filtered_data.groupby(['Company', 'Jaar'])['Totaal gespendeerd'].sum().reset_index()

#     # Maak de interactieve Plotly-grafiek
#     fig = px.bar(
#         totaal_per_bedrijf_jaar,
#         x='Company',
#         y='Totaal gespendeerd',
#         color='Jaar',
#         title="Totaal Bedrag per Bedrijf per Jaar",
#         labels={'Totaal gespendeerd': 'Totaal gespendeerd (€)', 'Company': 'Bedrijf'}
#     )

#     # Pas de layout aan voor betere visualisatie
#     fig.update_layout(
#         xaxis_title='Bedrijf',
#         yaxis_title='Totaal gespendeerd (€)',
#         legend_title='Jaar',
#         barmode='group',
#         hovermode='closest'
#     )

#     return fig

# # Start de Dash-app
# if __name__ == '__main__':
#     app.run_server(debug=True)
