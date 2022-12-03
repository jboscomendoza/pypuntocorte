import streamlit as st
import pandas as pd
import punto_corte as pc
 
st.set_page_config(page_title="Asistente para puntos de corte", page_icon=":shark:",
                   layout="centered", initial_sidebar_state="auto",
                   menu_items=None)
 
# Sidebar
st.sidebar.title("Archivo")
archivo = st.sidebar.file_uploader("Elige un archivo con columnas theta y error", type=["csv"])
if archivo is not None:
    #scores = pd.read_csv("dummy_short.csv")
    scores = pd.read_csv(archivo)
    scores = pc.crear_intervalos(scores)
    theta_min = scores["theta"].min()
    theta_max = scores["theta"].max()
 
# Main
if archivo is None:
    st.title("Elige un archivo para iniciar")
else:
    st.sidebar.title("Puntos de corte")
    contadores = st.sidebar.slider("Número de cortes", value=1,
                                   min_value=1, max_value=3)
   
    for i in range(contadores):
        nombre = f"Punto de corte {i+1}"
        clave = f"corte{i+1}"
        st.sidebar.number_input(nombre, value=theta_min,
                                min_value=theta_min, max_value=theta_max, key=clave)
   
    cortes = [st.session_state[f"corte{j+1}"] for j in range(contadores)]
 
    scores["grupos"] = pc.crear_grupos(scores, cortes)
    grupos_conteo = scores.groupby("grupos", as_index=False)["theta"].count()
 
    dist = pc.crear_dist(scores, cortes)
    pay = pc.crear_pay(grupos_conteo)
 
 
    st.subheader("Distribución")
    st.plotly_chart(dist, use_container_width=True)
 
 
    col1, col2 = st.columns([1, 1.5])
 
    col1.subheader("Proporción")
    col1.plotly_chart(pay, use_container_width=True)
    col2.subheader("Empalmes")
    col2.table(pc.df_empalmes(scores, cortes))
