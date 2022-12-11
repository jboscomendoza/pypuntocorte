import streamlit as st
import pandas as pd
import punto_corte as pc


st.set_page_config(page_title=u"Puntos de corte",
                   page_icon=":bar_chart:",
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)


st.markdown(u"# Puntos de corte")


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
    col_corte1, col_corte2 = st.columns(2)
    
    contadores = col_corte1.slider(
        u"Número de cortes", 
        value=1, 
        min_value=1, 
        max_value=3)
    
    for i in range(contadores):
        nombre_corte = f"Punto de corte {i+1}"
        clave = f"corte{i+1}"
        col_corte2.number_input(nombre_corte, 
                                value=puntaje.puntaje.min(),
                                min_value=puntaje.puntaje.min(), 
                                max_value=puntaje.puntaje.max(), 
                                key=clave)
    
    cortes = [st.session_state[f"corte{j+1}"] for j in range(contadores)]
    
    puntaje["grupos"] = pc.crear_grupos(puntaje, cortes)
    grupos_conteo = puntaje.groupby("grupos", as_index=False)["puntaje"].count()
 
    dist = pc.crear_dist(puntaje, cortes)
    pay = pc.crear_pay(grupos_conteo)
    
    st.markdown(u"### Distribución")
    st.plotly_chart(dist, use_container_width=True)

    col_plot1, col_plot2 = st.columns([1, 1.5])
    with col_plot1:
        st.markdown(u"### Proporción")
        st.plotly_chart(pay, use_container_width=True)
    with col_plot2:
        st.markdown(u"### Empalmes")
        st.table(pc.df_empalmes(puntaje, cortes))
