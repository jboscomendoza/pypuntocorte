import streamlit as st
import pandas as pd
import punto_corte as pc


try:
    shared = st.session_state["shared"]
except:
    st.error(u"No hay archivos cargados.")
    st.stop()


try:
    puntaje = st.session_state["puntaje"]
except:
    st.error(u"No hay archivo de puntaje cargado.")
else:
    st.markdown(u"### Resumen de los puntajes")
    st.table(puntaje.describe())
    st.markdown(u"### Distribución acumulada de los puntajes")
    st.plotly_chart(pc.crear_cumdist(puntaje, "puntaje"))