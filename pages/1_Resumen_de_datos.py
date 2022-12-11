import streamlit as st
import pandas as pd
import punto_corte as pc


st.set_page_config(page_title=u"Resumen de datos",
                   page_icon=":ledger:",
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)


st.markdown(u"# Resumen de datos")


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


try:
    items = st.session_state["items"]
except:
    st.error(u"No hay archivo de items cargado.")
else:
    st.markdown(u"### Resumen de los items")
    st.table(items.describe())
    st.markdown(u"### Distribución de dificultad")
    st.plotly_chart(pc.crear_cumdist(items, "items"))