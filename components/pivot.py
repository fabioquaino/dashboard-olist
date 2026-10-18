# Componente reutilizable para crear tablas dinámicas
from dash import html
from dash_pivottable import PivotTable


def crear_tabla_dinamica(datos):
    # Convertir los datos a registros para la tabla dinámica.
    registros = datos.to_dict("records")

    # Crear la tabla dinámica con campos iniciales.
    return html.Div(
        [
            PivotTable(
                id="tabla_dinamica_ventas",
                data=registros,
                rows=["product_category_name"],
                cols=["order_status"],
                vals=["price"],
                aggregatorName="Sum",
                rendererName="Table"
            )
        ],
        style={
            "backgroundColor": "white",
            "padding": "12px",
            "borderRadius": "8px",
            "overflowX": "auto"
        }
    )