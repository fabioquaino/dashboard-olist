# Vista temporal para secciones pendientes de desarrollo
from dash import html


def crear_vista_vacia(dashboard, vista):
    nombres_dashboard = {
        "ventas": "Ventas",
        "logistica": "Logística",
        "clientes": "Clientes"
    }

    nombres_vista = {
        "gerencial": "Gerencial",
        "analitica": "Analítica",
        "decisiones": "Decisiones"
    }

    return html.Div(
        [
            html.H3(
                f"{nombres_dashboard[dashboard]} - "
                f"{nombres_vista[vista]}",
                style={"marginTop": "0", "fontSize": "20px"}
            ),
            html.P(
                "Esta vista está pendiente de desarrollo.",
                style={"fontSize": "13px", "color": "#666"}
            )
        ],
        style={
            "padding": "20px",
            "backgroundColor": "white",
            "borderRadius": "8px"
        }
    )