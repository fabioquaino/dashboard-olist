# Callbacks para navegar entre dashboards y vistas
from dash import Input, Output

from views.gerencial.sales import crear_vista_gerencial_ventas
from views.analitica.sales import crear_vista_analitica_ventas
from views.placeholder import crear_vista_vacia


def registrar_callbacks_navegacion(app, anios, meses, df):

    # Volver a Gerencial cada vez que cambia el dashboard.
    @app.callback(
        Output("selector_vista", "value"),
        Input("selector_dashboard", "value")
    )
    def reiniciar_vista(dashboard):
        return "gerencial"

    # Mostrar la vista seleccionada.
    @app.callback(
        Output("contenedor_dashboard", "children"),
        Input("selector_dashboard", "value"),
        Input("selector_vista", "value")
    )
    def cambiar_vista(dashboard, vista):

        # Mostrar el dashboard gerencial de ventas.
        if dashboard == "ventas" and vista == "gerencial":
            return crear_vista_gerencial_ventas(anios, meses)

        # Mostrar el análisis de ventas.
        if dashboard == "ventas" and vista == "analitica":
            return crear_vista_analitica_ventas()

        # Mostrar una pantalla temporal para las demás combinaciones.
        return crear_vista_vacia(dashboard, vista)