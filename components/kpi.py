# Componentes visuales compactos para indicadores KPI
from dash import html

def formato_numero(valor):
    return f"{valor:,.0f}".replace(",", ".")

def crear_tarjeta(titulo, valor, id_valor):
    return html.Div(
        [
            html.P(
                titulo,
                style={
                    "margin": "0 0 6px 0",
                    "fontSize": "12px",
                    "color": "#666"
                }
            ),
            html.H3(
                valor,
                id=id_valor,
                style={
                    "margin": "0",
                    "fontSize": "23px",
                    "fontWeight": "600"
                }
            )
        ],
        style={
            "backgroundColor": "white",
            "padding": "12px 14px",
            "borderRadius": "8px",
            "boxShadow": "0 1px 5px #dddddd",
            "flex": "1",
            "minWidth": "0"
        }
    )