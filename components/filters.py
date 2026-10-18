# Componentes reutilizables para los filtros de fechas
from dash import dcc, html


def crear_filtros_fecha(anios, meses):

    # Preparar las opciones iniciales de los filtros.
    opciones_anio = [
        {"label": "Todos", "value": "__todos__"}
    ] + [
        {"label": str(anio), "value": int(anio)}
        for anio in anios
    ]

    opciones_trimestre = [
        {"label": "Todos", "value": "__todos__"},
        {"label": "1.er trimestre", "value": 1},
        {"label": "2.º trimestre", "value": 2},
        {"label": "3.er trimestre", "value": 3},
        {"label": "4.º trimestre", "value": 4}
    ]

    opciones_mes = [
        {"label": nombre, "value": numero}
        for numero, nombre in meses
    ]

    # Construir los controles de selección de fechas.
    return html.Div(
        [
            html.Div(
                [
                    html.Label("Modo de análisis"),
                    dcc.Dropdown(
                        id="filtro_modo_fecha",
                        options=[
                            {"label": "Anual", "value": "anual"},
                            {"label": "Mensual", "value": "mensual"}
                        ],
                        value="anual",
                        clearable=False
                    )
                ],
                style={"minWidth": "180px", "flex": "1"}
            ),
            html.Div(
                [
                    html.Label("Año"),
                    dcc.Dropdown(
                        id="filtro_anio",
                        options=opciones_anio,
                        value="__todos__",
                        clearable=False
                    )
                ],
                style={"minWidth": "140px", "flex": "1"}
            ),
            html.Div(
                [
                    html.Label("Trimestre"),
                    dcc.Dropdown(
                        id="filtro_trimestre",
                        options=opciones_trimestre,
                        value="__todos__",
                        clearable=False,
                        disabled=True
                    )
                ],
                id="contenedor_trimestre",
                style={"minWidth": "140px", "flex": "1"}
            ),
            html.Div(
                [
                    html.Label("Mes"),
                    dcc.Dropdown(
                        id="filtro_mes",
                        options=opciones_mes,
                        value=None,
                        clearable=False
                    )
                ],
                id="contenedor_mes",
                style={
                    "display": "none",
                    "minWidth": "140px",
                    "flex": "1"
                }
            )
        ],
        style={
            "display": "flex",
            "gap": "12px",
            "flexWrap": "wrap",
            "alignItems": "end"
        }
    )