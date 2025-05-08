import streamlit as st 
import time
import datetime
import numpy as np
from app_utils import predict
 


st.sidebar.image("Paull.png", use_container_width=True)
st.sidebar.title("Predicciones de Fútbol")
st.sidebar.markdown("""
Predice los resultados de partidos de fútbol. 
Selecciona la liga, los equipos, y la fecha del partido. Luego, haz clic en 
**"Predecir resultados"** para obtener las probabilidades de victoria.
""")

# Example: Add a selectbox in the sidebar
liga = st.sidebar.selectbox("Liga", ["LALIGA", "Premier League (Comming Soon)", "Ligue1 (Comming Soon)"])
predicciones = st.sidebar.multiselect('Predicciones (Comming Soon)', ['Resultados','Goles','Tarjetas'], default=['Resultados'])




st.markdown("<h1 style='text-align: center;'>PREDICE TU PARTIDO</h1>", unsafe_allow_html=True)
st.markdown("_____________________", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    home_team = st.selectbox('Local',['Elije un equipo'] + ['Alaves', 'Almeria', 'Athletic Club', 'Atletico Madrid',
        'Barcelona', 'Cadiz', 'Celta Vigo', 'Elche', 'Espanyol', 'Getafe',
        'Girona', 'Granada CF', 'Las Palmas', 'Levante', 'Mallorca',
        'Osasuna', 'Rayo Vallecano', 'Real Betis', 'Real Madrid',
        'Real Sociedad', 'Sevilla', 'Valencia', 'Valladolid', 'Villarreal'])


with col2:
    st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_allow_html=True)

with col3:
    away_team = st.selectbox('Visitante',['Elije un equipo'] + ['Alaves', 'Almeria', 'Athletic Club', 'Atletico Madrid',
        'Barcelona', 'Cadiz', 'Celta Vigo', 'Elche', 'Espanyol', 'Getafe',
        'Girona', 'Granada CF', 'Las Palmas', 'Levante', 'Mallorca',
        'Osasuna', 'Rayo Vallecano', 'Real Betis', 'Real Madrid',
        'Real Sociedad', 'Sevilla', 'Valencia', 'Valladolid', 'Villarreal'])
    
date = st.date_input('Game date', min_value=datetime.date(2021,1,1), max_value=datetime.date(2023,12,31)).strftime('%d/%m/%Y')

if home_team == 'Elije un equipo' or away_team == 'Elije un equipo':
    st.warning('Selecciona un equipo local y uno visitante')
elif home_team == away_team:
    st.error('Error: Ambos equipos no pueden ser el mismo')
else:

    
    bcol1, bcol2, bcol3 = st.columns([3, 2, 3])  # Adjust column widths as needed

    with bcol2:
        btn = st.button('Predecir resultados')
    if btn:
        progress_bar = st.progress(0)  # Initialize the progress bar
        for percent_complete in range(101):  # Loop from 0 to 100
            time.sleep(0.02)  # Simulate some work being done
            progress_bar.progress(percent_complete)  # Update the progress bar

        home_pred, draw_pred, away_pred = predict(home_team, away_team, date)

        st.markdown("_____________________", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center;'>Probabilidad de victoria</h3>", unsafe_allow_html=True)
        pcol1, pcol2, pcol3 = st.columns(3)

        with pcol1:
            st.markdown(f"<h3 style='text-align: center;'><u>     {home_team}     </u></h3>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: center;'>{home_pred}%</h4>", unsafe_allow_html=True)
        with pcol2:
            st.markdown("<h3 style='text-align: center;'><u>     Empate     </u></h3>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: center;'>{draw_pred}%</h4>", unsafe_allow_html=True)
        with pcol3:
            st.markdown(f"<h3 style='text-align: center;'><u>     {away_team}     </u></h3>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: center;'>{away_pred}%</h4>", unsafe_allow_html=True)