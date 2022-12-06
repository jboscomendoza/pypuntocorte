import streamlit as st
import pandas as pd
import punto_corte as pc
 
st.set_page_config(page_title="Asistente para puntos de corte",
                   page_icon=":shark:",
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)
  
# Main
archivo = None
tab_file, tab_vis = st.tabs(["Carga de archivo", "Visualización"])

if archivo is None:
    with tab_file:
        st.title("Elige un archivo para iniciar")
        st.subheader("Archivo")
        archivo = tab_file.file_uploader("Elige un archivo con columnas theta y error", type=["csv"])
        if archivo is not None:
            scores = pd.read_csv(archivo)
            scores = pc.crear_intervalos(scores)
            theta_min = scores["theta"].min()
            theta_max = scores["theta"].max()

if archivo is not None:
    st.sidebar.title("Puntos de corte")
    contadores = st.sidebar.slider("Número de cortes", value=1, min_value=1, max_value=3)
    
    for i in range(contadores):
        nombre_corte = f"Punto de corte {i+1}"
        clave = f"corte{i+1}"
        st.sidebar.number_input(nombre_corte, 
                                value=theta_min,
                                min_value=theta_min, 
                                max_value=theta_max, 
                                key=clave)
   
    cortes = [st.session_state[f"corte{j+1}"] for j in range(contadores)]

    scores["grupos"] = pc.crear_grupos(scores, cortes)
    grupos_conteo = scores.groupby("grupos", as_index=False)["theta"].count()
 
    dist = pc.crear_dist(scores, cortes)
    pay = pc.crear_pay(grupos_conteo)
    
    with tab_file:
        st.markdown("### Resumen de los puntajes")
        st.dataframe(scores.describe())
        st.markdown("### Distribución acumulada de los puntajes")
        st.plotly_chart(pc.crear_cumdist(scores))

    with tab_vis:
        st.subheader("Distribución")
        st.plotly_chart(dist, use_container_width=True)

        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.subheader("Proporción")
            st.plotly_chart(pay, use_container_width=True)
        with col2:
            st.subheader("Empalmes")
            st.table(pc.df_empalmes(scores, cortes))
