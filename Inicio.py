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



st.title("Elige tus archivos")
col_puntaje, col_items = st.columns(2)


if archivo_puntaje is None:
    col_puntaje.subheader("Puntajes")
    archivo_puntaje = col_puntaje.file_uploader(
        "Elige un archivo con columnas `puntaje` y `error`",
        type=["csv"])
    col_puntaje.markdown(f":floppy_disk: [Archivo muestra]({RUTA_PUNTAJE})")
    st.session_state["archivo_puntaje"] = archivo_puntaje


if archivo_puntaje is not None:
    puntaje = pd.read_csv(archivo_puntaje)
    puntaje_check = pc.es_valido(puntaje, "puntaje")
    if not puntaje_check["es_valido"]:
        col_puntaje.error(puntaje_check["mensaje"])
        st.stop()
    else:
        col_puntaje.success(puntaje_check["mensaje"])
        puntaje = pc.crear_intervalos(puntaje)
        st.session_state["puntaje"] = puntaje


if archivo_items is None:
    col_items.subheader("Items")
    archivo_items = col_items.file_uploader(
        "Elige un archivo con columnas `id` y `dificultad`",
        type=["csv"])
    col_items.markdown(f":floppy_disk: [Archivo muestra]({RUTA_ITEMS})")
    
if archivo_items is not None:
    items = pd.read_csv(archivo_items)
    items_check = pc.es_valido(items, "items")
    if not items_check["es_valido"]:
        col_items.error(items_check["mensaje"])
        st.stop()
    else:
        col_items.success(items_check["mensaje"])
        st.session_state["items"] = items