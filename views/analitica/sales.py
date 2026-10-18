# Vista analítica de ventas con agrupaciones configurables
from dash import html, dcc, dash_table


def crear_vista_analitica_ventas():
    # Definir las dimensiones disponibles para agrupar.
    dimensiones = [
        {"label": "Año", "value": "anio"},
        {"label": "Trimestre", "value": "trimestre"},
        {"label": "Mes", "value": "mes"},
        {"label": "Fecha", "value": "fecha"},
        {"label": "Categoría de producto", "value": "categoria"},
        {"label": "Vendedor", "value": "vendedor"},
        {"label": "Estado del pedido", "value": "estado"}
    ]

    # Definir las métricas disponibles.
    metricas = [
        {"label": "Facturación", "value": "facturacion"},
        {"label": "Cantidad de artículos", "value": "articulos"},
        {"label": "Pedidos únicos", "value": "pedidos"},
        {"label": "Compradores únicos", "value": "compradores"}
    ]

    # Preparar el selector de métricas.
    return html.Div(
        [
            html.Div(
                [
                    html.H2(
                        "Analítica de ventas",
                        style={"margin": "0 0 4px 0", "fontSize": "23px"}
                    ),
                    html.P(
                        "Configurá las agrupaciones y métricas para explorar las ventas.",
                        style={"margin": "0", "fontSize": "12px", "color": "#666"}
                    )
                ],
                style={"marginBottom": "18px"}
            ),

            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Agrupar por"),
                            dcc.Dropdown(
                                id="analitica_dimension",
                                options=dimensiones,
                                value="categoria",
                                clearable=False
                            )
                        ],
                        style={"flex": "1", "minWidth": "180px"}
                    ),
                    html.Div(
                        [
                            html.Label("Agrupación secundaria"),
                            dcc.Dropdown(
                                id="analitica_dimension_secundaria",
                                options=[
                                    {"label": "Ninguna", "value": "__ninguna__"}
                                ] + dimensiones,
                                value="__ninguna__",
                                clearable=False
                            )
                        ],
                        style={"flex": "1", "minWidth": "180px"}
                    ),
                    html.Div(
                        [
                            html.Label("Año"),
                            dcc.Dropdown(
                                id="analitica_anio",
                                options=[{"label": "Todos", "value": "__todos__"}],
                                value="__todos__",
                                clearable=False
                            )
                        ],
                        style={"flex": "1", "minWidth": "120px"}
                    ),
                    html.Div(
                        [
                            html.Label("Estado del pedido"),
                            dcc.Dropdown(
                                id="analitica_estado",
                                options=[{"label": "Todos", "value": "__todos__"}],
                                value="__todos__",
                                clearable=False
                            )
                        ],
                        style={"flex": "1", "minWidth": "160px"}
                    )
                ],
                style={
                    "display": "flex",
                    "gap": "12px",
                    "flexWrap": "wrap",
                    "marginBottom": "14px"
                }
            ),

            html.Div(
                [
                    html.Label("Métricas"),
                    dcc.Checklist(
                        id="analitica_metricas",
                        options=metricas,
                        value=["facturacion", "pedidos"],
                        inline=True,
                        style={"display": "flex", "gap": "18px", "flexWrap": "wrap"}
                    )
                ],
                style={
                    "backgroundColor": "white",
                    "padding": "12px",
                    "borderRadius": "8px",
                    "marginBottom": "14px"
                }
            ),

            html.Div(
                [
                    dash_table.DataTable(
                        id="tabla_analitica_ventas",
                        columns=[],
                        data=[],
                        page_size=15,
                        sort_action="native",
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "padding": "9px",
                            "textAlign": "left",
                            "fontFamily": "Arial",
                            "fontSize": "13px",
                            "minWidth": "100px",
                            "width": "150px",
                            "maxWidth": "280px",
                            "whiteSpace": "normal",
                            "height": "auto"
                        },
                        style_header={
                            "fontWeight": "bold",
                            "backgroundColor": "#f0f2f5",
                            "textAlign": "left"
                        },
                        # Mantener anchos estables para dimensiones y métricas
                        style_cell_conditional=[
                            {
                                "if": {"column_type": "text"},
                                "width": "220px",
                                "minWidth": "220px",
                                "maxWidth": "220px"
                            },
                            {
                                "if": {"column_type": "numeric"},
                                "width": "150px",
                                "minWidth": "150px",
                                "maxWidth": "150px"
                            }
                        ]
                    )
                ],
                style={
                    "backgroundColor": "white",
                    "padding": "12px",
                    "borderRadius": "8px",
                    "marginBottom": "14px",
                    "boxShadow": "0 1px 5px #dddddd"
                }
            ),

            html.Div(
                [
                    dcc.Graph(
                        id="grafico_analitica_ventas",
                        config={"displayModeBar": False},
                        style={"height": "350px"}
                    )
                ],
                style={
                    "backgroundColor": "white",
                    "padding": "12px",
                    "borderRadius": "8px",
                    "boxShadow": "0 1px 5px #dddddd"
                }
            )
        ],
        style={
            "fontFamily": "Arial",
            "padding": "14px 20px",
            "boxSizing": "border-box"
        }
    )