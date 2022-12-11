import streamlit as st
import pandas as pd
import punto_corte as pc
 

st.set_page_config(page_title="Asistente para puntos de corte",
                   page_icon=":bookmark_tabs:",
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)


# Inicio de sesion compartida
if "shared" not in st.session_state:
   st.session_state["shared"] = True

 
archivo_puntaje = None
archivo_items = None

RUTA_EJEMPLO = "https://raw.githubusercontent.com/jboscomendoza/pypuntocorte/main/"
RUTA_PUNTAJE  = RUTA_EJEMPLO + "irt_puntaje.csv"
RUTA_ITEMS    = RUTA_EJEMPLO + "irt_items.csv"


# Main
tab_file, tab_wright = st.tabs([
    u":file_folder: Carga de archivos",
    u":scroll: Mapa de Wright"])
tab_file.title("Elige tus archivos")

with tab_file:
    col_file_puntaje, col_file_items = st.columns(2)

if archivo_puntaje is None:
    col_file_puntaje.subheader("Puntajes")
    archivo_puntaje = col_file_puntaje.file_uploader(
        "Elige un archivo con columnas `puntaje` y `error`",
        type=["csv"])
    col_file_puntaje.markdown(f":floppy_disk: [Archivo muestra]({RUTA_PUNTAJE})")
    st.session_state["archivo_puntaje"] = archivo_puntaje
    
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
    st.session_state["puntaje"] = puntaje
       
if archivo_items is None:
    col_file_items.subheader("Items")
    archivo_items = col_file_items.file_uploader(
        "Elige un archivo con columnas `id` y `dificultad`",
        type=["csv"])
col_file_items.markdown(f":floppy_disk: [Archivo muestra]({RUTA_ITEMS})")
if archivo_items is not None:
    items = pd.read_csv(archivo_items)
    items_check = pc.es_valido(items, "items")
    if not items_check["es_valido"]:
        st.stop() 
    col_file_items.markdown(items_check["mensaje"])
    st.session_state["items"] = items


if all([archivo_puntaje, archivo_items]):
    tab_wright.markdown("# Mapa de Wright")
    mapa_wright = pc.crear_mapa_wright(puntaje, items)
    tab_wright.plotly_chart(mapa_wright)