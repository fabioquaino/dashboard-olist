# Callbacks para la vista analítica de ventas
from dash import Input, Output
import plotly.express as px

from data.sales import consultar_ventas_agrupadas


def registrar_callbacks_analitica_ventas(app, df):
    # Preparar las opciones de los filtros.
    anios = sorted(df["anio"].dropna().astype(int).unique())
    estados = sorted(df["order_status"].dropna().unique())

    opciones_anio = [{"label": "Todos", "value": "__todos__"}] + [
        {"label": str(anio), "value": int(anio)} for anio in anios
    ]
    opciones_estado = [{"label": "Todos", "value": "__todos__"}] + [
        {"label": estado, "value": estado} for estado in estados
    ]

    # Cargar las opciones de los filtros cuando aparece la vista.
    @app.callback(
        Output("analitica_anio", "options"),
        Output("analitica_estado", "options"),
        Input("selector_vista", "value")
    )
    def cargar_opciones_filtros(vista):
        return opciones_anio, opciones_estado

    # Actualizar la tabla y el gráfico según la configuración seleccionada.
    @app.callback(
        Output("tabla_analitica_ventas", "columns"),
        Output("tabla_analitica_ventas", "data"),
        Output("grafico_analitica_ventas", "figure"),
        Input("analitica_dimension", "value"),
        Input("analitica_dimension_secundaria", "value"),
        Input("analitica_anio", "value"),
        Input("analitica_estado", "value"),
        Input("analitica_metricas", "value")
    )
    def actualizar_analisis(dimension, secundaria, anio, estado, metricas):
        
        # Definir los nombres visibles de las métricas
        nombres_metricas = {
            "facturacion": "Facturación",
            "articulos": "Cantidad de artículos",
            "pedidos": "Pedidos únicos",
            "compradores": "Compradores únicos"
        }
        
        # Evitar consultas si no hay métricas seleccionadas.
        if not metricas:
            figura = px.bar(title="Seleccioná al menos una métrica")
            figura.update_layout(template="plotly_white")
            return [], [], figura

        # Convertir las opciones que representan "todos" o "ninguna".
        secundaria = None if secundaria == "__ninguna__" else secundaria
        anio = None if anio == "__todos__" else anio
        estado = None if estado == "__todos__" else estado

        # Consultar los datos ya agrupados en PostgreSQL.
        df_analisis = consultar_ventas_agrupadas(
            dimension=dimension,
            dimension_secundaria=secundaria,
            metricas=metricas,
            anio=anio,
            estado=estado
        )

        # Preparar la tabla.
        columnas = [
            {
                "name": columna,
                "id": columna,
                "type": "numeric" if columna in nombres_metricas.values() else "text"
            }
            for columna in df_analisis.columns
        ]
        datos = df_analisis.to_dict("records")

        nombre_metrica = nombres_metricas[metricas[0]]

        # Verificar que la métrica exista en el resultado.
        if nombre_metrica not in df_analisis.columns:
            figura = px.bar(title="No se encontró la métrica seleccionada")
            figura.update_layout(template="plotly_white")
            return columnas, datos, figura

        # Identificar la dimensión principal.
        columnas_metricas = list(nombres_metricas.values())
        nombre_dimension = next(
            columna for columna in df_analisis.columns
            if columna not in columnas_metricas
        )

        # Crear siempre gráficos de barras verticales
        if df_analisis.empty:
            figura = px.bar(title="No hay datos para los filtros seleccionados")
        else:
            datos_grafico = df_analisis.copy()

            nombres_dimensiones = {
                "anio": "Año",
                "trimestre": "Trimestre",
                "mes": "Mes",
                "fecha": "Fecha",
                "categoria": "Categoría",
                "vendedor": "Vendedor",
                "estado": "Estado"
            }

            hay_doble_agrupacion = (
                secundaria is not None and secundaria != dimension
            )

            if hay_doble_agrupacion:
                nombre_dimension_secundaria = nombres_dimensiones[secundaria]

                # Tratar la segunda dimensión como categoría, incluso si es numérica.
                datos_grafico[nombre_dimension_secundaria] = (
                    datos_grafico[nombre_dimension_secundaria].astype(str)
                )

                figura = px.bar(
                    datos_grafico,
                    x=nombre_dimension,
                    y=nombre_metrica,
                    color=nombre_dimension_secundaria,
                    barmode="group",
                    title=nombre_metrica,
                    hover_data=[nombre_dimension, nombre_dimension_secundaria]
                )
            else:
                datos_grafico = datos_grafico.sort_values(
                    nombre_metrica, ascending=False
                ).head(20)

                figura = px.bar(
                    datos_grafico,
                    x=nombre_dimension,
                    y=nombre_metrica,
                    title=nombre_metrica,
                    hover_data=[nombre_dimension]
                )

        figura.update_layout(
            template="plotly_white",
            margin={"l": 20, "r": 20, "t": 50, "b": 20},
            xaxis_title=nombre_dimension,
            yaxis_title=nombre_metrica
        )
        
        # Evitar valores intermedios en el eje X
        figura.update_xaxes(type="category")

        return columnas, datos, figura