import streamlit as st
import pandas as pd
import plotly.express as px

# Zet de titel en layout van de app
st.set_page_config(page_title="Bedrijven Inkoop Analyse", layout="wide")

# Functie om de data in te laden en voor te bereiden
@st.cache_data
def load_data():
    df = pd.read_csv('NoteBooks/Data/inkoop.csv')
    df['Datum'] = pd.to_datetime(df['Datum'], format="%d/%m/%Y", errors='coerce')
    df['Jaar'] = df['Datum'].dt.year
    df['Totaal gespendeerd'] = df['Totaal gespendeerd'].replace({'€': '', ',': ''}, regex=True).astype(float)
    return df

# Laad de data
df = load_data()


# Sidebar-menu voor navigatie tussen pagina's
st.sidebar.title("Navigatie")
pagina = st.sidebar.radio("Ga naar", ["Home 🏠", "Inkoop 💸"])

# Home-pagina met uitleg
if pagina == "Home 🏠":
    st.title("Bedrijven Inkoop Analyse")
    st.write("""
    Welkom bij de Bedrijven Inkoop Analyse App. Deze applicatie toont een overzicht van de totale bestedingen 
    per bedrijf over meerdere jaren, met de mogelijkheid om gegevens voor specifieke jaren en bedrijven te selecteren.
    
    Gebruik het menu aan de zijkant om te navigeren tussen de verschillende pagina's.
    """)

# Inkoop-pagina met grafieken
elif pagina == "Inkoop 💸":
    st.title("Inkoop Overzicht per Bedrijf")
    
    # Filteropties: selecteer jaar en bedrijf
    jaren_selectie = st.multiselect("Selecteer jaar", options=df['Jaar'].unique(), default=df['Jaar'].unique())
    bedrijven_selectie = st.multiselect("Selecteer bedrijven", options=df['Company'].unique(), default=df['Company'].unique())
    
    # Filter de data op basis van de selectie
    gefilterde_data = df[(df['Jaar'].isin(jaren_selectie)) & (df['Company'].isin(bedrijven_selectie))]
    
    # Groepeer de gefilterde data per bedrijf en jaar en bereken de totaalbedragen
    totaal_per_bedrijf_jaar = gefilterde_data.groupby(['Company', 'Jaar'])['Totaal gespendeerd'].sum().reset_index()
    
    # Maak de interactieve Plotly-grafiek
    fig = px.bar(
        totaal_per_bedrijf_jaar,
        x='Company', 
        y='Totaal gespendeerd', 
        color='Jaar',
        title="Totaal Bedrag per Bedrijf per Jaar",
        labels={'Totaal gespendeerd': 'Totaal gespendeerd (€)', 'Company': 'Bedrijf'}
    )
    
    # Toon de grafiek in de app
    st.plotly_chart(fig, use_container_width=True)

    # Extra uitleg of data weergeven
    st.write("De grafiek hierboven toont de totale uitgaven per bedrijf voor de geselecteerde jaren.")
