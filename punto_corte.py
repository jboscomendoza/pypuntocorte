import pandas as pd
import plotly.graph_objects as go
 
 
COLORES = ["#ff595e", "#ffca3a", "#8ac926", "#1982c4"]
 
 
def crear_intervalos(datos):
    spread = datos["error"] * 1.96
    datos["lim_inf"] = datos["theta"] - spread
    datos["lim_sup"] = datos["theta"] + spread
    return datos
 
 
def crear_grupos(datos, puntos_corte):
    theta = datos["theta"]
    puntos_corte = puntos_corte + [theta.min(), theta.max()]
    puntos_corte = [*set(puntos_corte)]
    puntos_corte.sort()
    num_grupos = len(puntos_corte) - 1
    if num_grupos > 1:
        nombres = [f"Grupo {i+1}" for i in range(0, num_grupos)]
        grupos = pd.cut(theta, puntos_corte, labels = nombres, include_lowest=True,
                        duplicates="drop")
    else:
        nombres = ["Grupo único"]
        grupos = pd.cut(theta, 1, labels = nombres)
    return grupos
 
 
def obtener_empalmes(datos, punto_corte):
    set_1 = datos[["lim_inf", "theta"]] > punto_corte
    set_1 = set_1.all(axis=1)
    set_2 = datos[["lim_sup", "theta"]] < punto_corte
    set_2 = set_2.all(axis=1)
    personas = len(datos)
    empalmes = personas - sum(sum([set_1, set_2]))
    proporcion = round(empalmes / personas, 2) * 100
    empalmes = dict(punto_corte=punto_corte,
                personas=personas, empalmes=empalmes,
                proporcion=proporcion)
    return empalmes
 
 
def df_empalmes(datos, punto_corte):
    empalmes = pd.DataFrame([obtener_empalmes(datos, i) for i in punto_corte])
    return empalmes
 
 
def crear_pay(datos_conteo, colores=COLORES):
    pay = go.Figure(data=[go.Pie(
    labels=list(datos_conteo["grupos"]), values=datos_conteo["theta"],
    textinfo="label+percent", textposition="inside",
    hole=.4,
    marker=dict(
        colors=colores,
        line=dict(color='#333333', width=1.5)
        )
    )])
    pay.update_layout(
        height=250,
        margin=dict(t=0, b=0, l=15, r=35)
    )
    return pay
   
 
def crear_dist(datos_scores, puntos_corte):
    dist = go.Figure()
    dist.add_trace(go.Violin(x=datos_scores["theta"], y0="Puntaje",
                        points="all", jitter=0.05,
                        line_color="#eeeeee", fillcolor="#bde0fe",
                        opacity=0.5))
    for i in range(len(puntos_corte)):
        dist.add_vline(puntos_corte[i], line_color=COLORES[i])
    dist.update_layout(
        height=250,
        margin=dict(t=35, b=35, l=55, r=15),
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return dist