# Punto de entrada de la aplicación Dash
from dash import Dash, html

from data.sales import cargar_ventas
from callbacks.sales import registrar_callbacks_ventas
from callbacks.navigation import registrar_callbacks_navegacion
from components.navigation import crear_barra_navegacion

# Importar los callbacks de analítica
from callbacks.analytics import registrar_callbacks_analitica_ventas




# Cargar los datos preparados desde Supabase.
df = cargar_ventas()

# Obtener los años disponibles como números enteros
anios = sorted(df["anio"].dropna().astype(int).unique())

# Definir los nombres de los meses.
meses = [
    (1, "Enero"),
    (2, "Febrero"),
    (3, "Marzo"),
    (4, "Abril"),
    (5, "Mayo"),
    (6, "Junio"),
    (7, "Julio"),
    (8, "Agosto"),
    (9, "Septiembre"),
    (10, "Octubre"),
    (11, "Noviembre"),
    (12, "Diciembre")
]

# Crear la aplicación y permitir vistas con componentes dinámicos.
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dashboard Olist"

# Definir la estructura general del dashboard.
app.layout = html.Div(
    [
        crear_barra_navegacion(),
        html.Div(
            id="contenedor_dashboard",
            style={"padding": "0 20px 20px 20px"}
        )
    ],
    style={
        "fontFamily": "Arial",
        "backgroundColor": "#f5f6fa",
        "minHeight": "100vh"
    }
)

# Registrar los callbacks de cada módulo.
registrar_callbacks_ventas(app, df)
registrar_callbacks_navegacion(app, anios, meses, df)
registrar_callbacks_analitica_ventas(app, df)

# Iniciar el servidor local.
if __name__ == "__main__":
    app.run(debug=True)