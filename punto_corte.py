import pandas as pd
import plotly.graph_objects as go


COLORES = ["#ff595e", "#ffca3a", "#8ac926", "#1982c4"]
 
 
def crear_intervalos(datos: pd.DataFrame) -> pd.DataFrame:
    """Agrega los límites inferior y superior del puntaje a partir del error
    de medición. 
    DataFrame con puntajes de persona y error de medición.

    Args:
        datos (pd.DataFrame): DataFrame con una columna llamada `theta` y 
        otra columna llamada `error`.

    Returns:
        pd.DataFrame: DataFrame `datos`con dos columnas adicionales, `lin_inf` 
        y `lim_sup`, límite inferior y superior con respecto al error de 
        medición, respectivamente.
    """
    spread = datos["error"]
    datos_intervalos = datos
    datos_intervalos["lim_inf"] = datos["theta"] - spread
    datos_intervalos["lim_sup"] = datos["theta"] + spread
    return datos_intervalos
 
 
def crear_grupos(datos: pd.DataFrame, puntos_corte: list) -> pd.Series:
    """Crea una columna que clasifica valores en grupos (bins) a partir de 
    puntos de corte definidos.
    
    Si no es posible crear al menos dos grupos con los puntos de corte 
    definidos, por ejemplo, cuando todos los cortes son iguales al valor más 
    pequeño, se crea un grupo único.

    Args:
        datos (pd.DataFrame): DataFrame con una columna llamada `theta` que 
        contiene puntajes de personas.
        puntos_corte (list): Lista de puntos de corte.

    Returns:
        pd.Series: Series que contiene los datos de la columna `theta` grupos 
        (bins) obtenidos.
        
    """
    theta = datos["theta"]
    puntos_corte = puntos_corte + [theta.min(), theta.max()]
    # Flatten
    puntos_corte = [*set(puntos_corte)] 
    puntos_corte.sort()
    num_grupos = len(puntos_corte) - 1
    if num_grupos > 1:
        nombres = [f"Grupo {i+1}" for i in range(0, num_grupos)]
        grupos = pd.cut(
            theta,
            puntos_corte,
            labels=nombres,
            include_lowest=True,
            duplicates="drop")
    else:
        nombres = ["Grupo único"]
        grupos = pd.cut(theta, 1, labels = nombres)
    return grupos
 
 
def obtener_empalmes(datos: pd.DataFrame, punto_corte: float) -> dict:
    """"Calcula el numero de personas que tienen puntajes cuyos límite iferior
    y superior con respecto al error empalman con un punto de corte definido."""
    set_1 = datos[["lim_inf", "theta"]] > punto_corte
    set_1 = set_1.all(axis=1)
    set_2 = datos[["lim_sup", "theta"]] < punto_corte
    set_2 = set_2.all(axis=1)
    personas = len(datos)
    empalmes = personas - sum(sum([set_1, set_2]))
    proporcion = round(empalmes / personas, 2) * 100
    empalmes = dict(
        punto_corte=punto_corte,
        personas=personas, 
        empalmes=empalmes,
        proporcion=proporcion
        )
    return empalmes
 
 
def df_empalmes(datos: pd.DataFrame, punto_corte: list) -> pd.DataFrame:
    """"Calcula el numero de personas que tienen puntajes cuyos límites superior
    o infeerior con respecto al error de medición empalman con uno o más puntos 
    de corte definidos.

    Args:
        datos (pd.DataFrame): DataFrame con columnas `theta`, `lim_inf` y 
        `lim_sup`.
        punto_corte (list): Valor de un punto de corte.

    Returns:
        pd.DataFrame: DataFrame que contiene el valor del punto, total de personas con 
        puntaje cantidad de personas cuyos puntajes se empalman con el punto de 
        corte y la proporción que representa con respecto al total
    """
    empalmes = pd.DataFrame([obtener_empalmes(datos, i) for i in punto_corte])
    return empalmes
 
 
def crear_pay(datos_conteo: pd.DataFrame, colores: str=COLORES) -> go.Figure:
    """Genera una gráfica de pastel con el conteo de personas que fueron asignadas 
    a cada grupo a partir de puntos de corte definidos.

    Args:
        datos_conteo (pd.DataFrame): DataFrame con el conteo personas asigandas a cada grupo.
        colores (str, optional): Colores de cada grupo. Hasta cuatro. Defaults to COLORES.

    Returns:
        go.Figure: Gráfica de pastel.
    """
    pay = go.Figure(data=[
        go.Pie(
            labels=list(datos_conteo["grupos"]),
            values=datos_conteo["theta"],
            textinfo="label+percent",
            textposition="inside",
            marker=dict(
                colors=colores,
                line=dict(color='#333333', width=1.5)),
            hole=.35)
        ])
    pay.update_layout(
        height=250,
        margin=dict(t=0, b=0, l=15, r=35))
    return pay
   
 
def crear_dist(datos_scores: pd.DataFrame, puntos_corte: list) -> go.Figure:
    """Genera una gráfica de violín que muestra la distribución de puntajes de 
    las personas y la posiciónd de los puntos de corte definidos.

    Args:
        datos_scores (pd.DataFrame): DataFrame con columna `theta`.
        puntos_corte (list): Puntos de corte definidos.

    Returns:
        go.Figure: Gráfica de violín.
    """
    dist = go.Figure()
    dist.add_trace(
        go.Violin(
            x=datos_scores["theta"],
            y0="Puntaje",
            line_color="#eeeeee", 
            fillcolor="#bde0fe",
            opacity=0.45,
            points="all",
            jitter=0.2,
            marker=dict(
                color="#bde0fe",
                size=2,
                opacity=.65),
            hoverinfo="skip")
        )
    for i in range(len(puntos_corte)):
        dist.add_vline(puntos_corte[i], 
                       line_color=COLORES[i])
    dist.update_layout(height=300,
                       margin=dict(t=35, b=35, l=55, r=15),
                       plot_bgcolor="rgba(0,0,0,0)")
    return dist


def crear_cumdist(datos: pd.DataFrame) -> go.Figure:
    """Crea una gráfica de distribución acumulada de puntajes"""
    datos_orden = datos.sort_values("theta", ignore_index=True).reset_index()
    cumdist = go.Figure()
    cumdist.add_trace(go.Scatter(
        name="Theta",
        x=datos_orden["index"],
        y=datos_orden["theta"],
        mode="lines",
        marker=dict(color="rgba(110, 120, 135, 255)")))
    cumdist.add_trace(go.Scatter(
        name="Límite superior",
        x=datos_orden["index"],
        y=datos_orden["lim_sup"],
        mode="lines",
        line=dict(width=0),
        marker=dict(color="rgba(210, 210, 220, 40)"),
        showlegend=False))
    cumdist.add_trace(go.Scatter(
        name="Límite inferior",
        x=datos_orden["index"],
        y=datos_orden["lim_inf"],
        mode="lines",
        line=dict(width=0),
        marker=dict(color="rgba(210, 210, 220, 40)"),
        showlegend=False,
        fill="tonexty"))
    cumdist.update_layout(
        hovermode="x",
        height=320,
        margin=dict(t=35, b=35, l=55, r=15),
        plot_bgcolor="rgba(0,0,0,0)")
    return cumdist


def crear_mapa_wright(datos_puntaje: pd.DataFrame, datos_items: pd.DataFrame) -> go.Figure:
    """Crea un mapa de Wright con datos de puntaje de personas y dificultad de ítems"""
    datos_puntaje["eje"] = 0
    datos_items["eje"]   = 0
    
    mapa_wright=go.Figure()
    mapa_wright.add_trace(go.Violin(
        x=datos_puntaje["eje"],
        y=datos_puntaje["theta"], 
        name="Personas",
        side="negative",
        fillcolor="#bde0fe",
        line_color="#68b7fd",
        width=3
    ))
    mapa_wright.add_trace(go.Violin(
        x=datos_items["eje"],
        y=datos_items["dificultad"], 
        name='Items',
        side="positive",
        fillcolor="rgba(0, 0, 0, 0)",
        line_color="rgba(0, 0, 0, 0)",
        text=list(datos_items["id"]),
        hoverinfo="text+y",
        points="all", 
        pointpos=0.05, 
        jitter=0,
        marker=dict(
            color = "#f4a261", 
            line=dict(
                width=1, 
                color="#777"),
            size=12, 
            symbol="triangle-left"),
        width=0)
    )
    mapa_wright.update_layout(
        violingap=0, 
        violinmode='overlay',
        margin=dict(t=35, b=35, l=55, r=15))
    
    return mapa_wright