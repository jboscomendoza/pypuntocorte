import streamlit as st
import pandas as pd
import punto_corte as pc


st.set_page_config(page_title=u"Mapa de Wright",
                   page_icon=":scroll:",
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)


st.markdown(u"# Mapa de Wright")


try:
    shared = st.session_state["shared"]
except:
    st.error(u"No hay archivos cargados.")
    st.stop()


puntaje_ok, items_ok = False, False


try:
    puntaje = st.session_state["puntaje"]
    puntaje_ok = True
except:
    st.error(u"Es necesario el archivo de puntaje.")


try:
    items = st.session_state["items"]
    items_ok = True
except:
    st.error(u"Es necesario el archivo de items.")


if(all([puntaje_ok, items_ok])):
    mapa_wright = pc.crear_mapa_wright(puntaje, items)
    st.plotly_chart(mapa_wright)