import streamlit as st
import pandas as pd
import punto_corte as pc
 
st.set_page_config(page_title="Asistente para puntos de corte",
                   page_icon=":bookmark_tabs:",
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)
  
archivo_puntaje = None
archivo_items = None

ruta_ejemplo = "https://raw.githubusercontent.com/jboscomendoza/pypuntocorte/main/"
ruta_puntaje  = ruta_ejemplo + "irt_puntaje.csv"
ruta_items   = ruta_ejemplo + "irt_items.csv"


# Main
tab_file, tab_vis, tab_wright = st.tabs([
    ":floppy_disk: Carga de archivos", 
    ":bar_chart: Visualización",
    ":scroll: Mapa de Wright"])
tab_file.title("Elige tus archivos")

with tab_file:
    col_file_puntaje, col_file_items = st.columns(2)

if archivo_puntaje is None:    
    col_file_puntaje.subheader("Puntajes")
    archivo_puntaje = col_file_puntaje.file_uploader(
        "Elige un archivo con columnas `puntaje` y `error`",
        type=["csv"])
    col_file_puntaje.markdown(f":floppy_disk: [Archivo muestra]({ruta_puntaje})")
if archivo_puntaje is not None:
    puntaje = pd.read_csv(archivo_puntaje)
    puntaje_check = pc.es_valido(puntaje, "puntaje")
    if not puntaje_check["es_valido"]:
        col_file_puntaje.markdown(puntaje_check["mensaje"])
        st.stop()    
    col_file_puntaje.markdown(puntaje_check["mensaje"])
    puntaje = pc.crear_intervalos(puntaje)
    puntaje_min = puntaje["puntaje"].min()
    puntaje_max = puntaje["puntaje"].max()
   
if archivo_items is None:
    col_file_items.subheader("Items")
    archivo_items = col_file_items.file_uploader(
        "Elige un archivo con columnas `id` y `dificultad`",
        type=["csv"])
col_file_items.markdown(f":floppy_disk: [Archivo muestra]({ruta_items})")
if archivo_items is not None:
    items = pd.read_csv(archivo_items)
    items_check = pc.es_valido(items, "items")
    if not items_check["es_valido"]:
        st.stop() 
    col_file_items.markdown(items_check["mensaje"])
        

if archivo_puntaje is not None:
    st.sidebar.title("Puntos de corte")
    contadores = st.sidebar.slider(
        "Número de cortes", 
        value=1, 
        min_value=1, 
        max_value=3)
    
    for i in range(contadores):
        nombre_corte = f"Punto de corte {i+1}"
        clave = f"corte{i+1}"
        st.sidebar.number_input(nombre_corte, 
                                value=puntaje_min,
                                min_value=puntaje_min, 
                                max_value=puntaje_max, 
                                key=clave)
   
    cortes = [st.session_state[f"corte{j+1}"] for j in range(contadores)]

    puntaje["grupos"] = pc.crear_grupos(puntaje, cortes)
    grupos_conteo = puntaje.groupby("grupos", as_index=False)["puntaje"].count()
 
    dist = pc.crear_dist(puntaje, cortes)
    pay = pc.crear_pay(grupos_conteo)
    
    col_file_puntaje.markdown("### Resumen de los puntajes")
    col_file_puntaje.dataframe(puntaje.describe())
            
    with tab_file:
        st.markdown("### Distribución acumulada de los puntajes")
        st.plotly_chart(pc.crear_cumdist(puntaje))

    with tab_vis:
        st.subheader("Distribución")
        st.plotly_chart(dist, use_container_width=True)

        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.subheader("Proporción")
            st.plotly_chart(pay, use_container_width=True)
        with col2:
            st.subheader("Empalmes")
            st.table(pc.df_empalmes(puntaje, cortes))

if archivo_items is not None:
    col_file_items.markdown("### Resumen de items")
    col_file_items.dataframe(items.describe())
    
if all([archivo_puntaje, archivo_items]):
    tab_wright.markdown("# Mapa de Wright")
    mapa_wright = pc.crear_mapa_wright(puntaje, items)
    tab_wright.plotly_chart(mapa_wright)