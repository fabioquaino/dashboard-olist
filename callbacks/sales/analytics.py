
# Callbacks para la vista analítica de ventas
from dash import Input, Output
import plotly.express as px

from data.sales import consultar_ventas_agrupadas


def registrar_callbacks_analitica_ventas(app, df):

    # Preparar las opciones de los filtros.
    anios = sorted(df["anio"].dropna().astype(int).unique())

    opciones_anio = [
        {"label": "Todos", "value": "__todos__"}
    ] + [
        {"label": str(anio), "value": int(anio)}
        for anio in anios
    ]

    opciones_estado = [
        {"label": "Todos", "value": "__todos__"},
        {"label": "Entregado", "value": "__entregado__"},
        {"label": "En proceso", "value": "__en_proceso__"}
    ]

    # Cargar las opciones de los filtros cuando aparece la vista.
    @app.callback(
        Output("analitica_anio", "options"),
        Output("analitica_estado", "options"),
        Input("selector_vista", "value")
    )
    def cargar_opciones_filtros(vista):
        return opciones_anio, opciones_estado

    # Actualizar la tabla, sus estilos y el gráfico.
    @app.callback(
        Output("tabla_analitica_ventas", "columns"),
        Output("tabla_analitica_ventas", "data"),
        Output("tabla_analitica_ventas", "style_data_conditional"),
        Output("grafico_analitica_ventas", "figure"),
        Input("analitica_dimension", "value"),
        Input("analitica_dimension_secundaria", "value"),
        Input("analitica_anio", "value"),
        Input("analitica_estado", "value"),
        Input("analitica_metricas", "value")
    )
    def actualizar_analisis(
        dimension, secundaria, anio, estado, metricas
    ):

        # Definir los nombres visibles de las métricas y dimensiones.
        nombres_metricas = {
            "facturacion": "Facturación",
            "articulos": "Cantidad de artículos",
            "pedidos": "Pedidos únicos",
            "compradores": "Compradores únicos"
        }

        nombres_dimensiones = {
            "anio": "Año",
            "trimestre": "Trimestre",
            "mes": "Mes",
            "fecha": "Fecha",
            "categoria": "Categoría",
            "vendedor": "Vendedor",
            "estado": "Estado"
        }

        # Evitar consultas si no hay métricas seleccionadas.
        if not metricas:
            figura = px.bar(
                title="Seleccioná al menos una métrica"
            )
            figura.update_layout(template="plotly_white")
            return [], [], [], figura

        # Convertir las opciones que representan "todos" o "ninguna".
        secundaria = (
            None if secundaria == "__ninguna__"
            else secundaria
        )

        anio = None if anio == "__todos__" else anio

        # Consultar los datos agrupados en PostgreSQL.
        # La función SQL deberá interpretar los tres valores de estado.
        df_analisis = consultar_ventas_agrupadas(
            dimension=dimension,
            dimension_secundaria=secundaria,
            metricas=metricas,
            anio=anio,
            estado=estado
        )

        # Identificar las columnas de las dimensiones seleccionadas.
        nombre_dimension = nombres_dimensiones[dimension]

        hay_doble_agrupacion = (
            secundaria is not None and secundaria != dimension
        )

        nombre_dimension_secundaria = (
            nombres_dimensiones[secundaria]
            if hay_doble_agrupacion
            else None
        )

        # Calcular variaciones cuando la dimensión principal es temporal.
        calcular_variacion = (
            dimension in ("mes", "anio")
            or (dimension == "trimestre" and anio is not None)
        )

        if calcular_variacion and not df_analisis.empty:

            # Ordenar cronológicamente dentro de cada grupo secundario.
            columnas_orden = (
                [nombre_dimension_secundaria, nombre_dimension]
                if hay_doble_agrupacion
                else [nombre_dimension]
            )

            df_analisis = df_analisis.sort_values(
                columnas_orden
            ).copy()

            # Calcular diferencias absolutas y porcentuales por métrica.
            for metrica in metricas:
                nombre = nombres_metricas[metrica]

                if hay_doble_agrupacion:
                    anterior = df_analisis.groupby(
                        nombre_dimension_secundaria,
                        dropna=False
                    )[nombre].shift(1)
                else:
                    anterior = df_analisis[nombre].shift(1)

                diferencia = df_analisis[nombre] - anterior

                # No calcular porcentaje cuando el valor anterior es cero.
                porcentaje = (
                    diferencia / anterior.where(anterior != 0)
                ) * 100

                df_analisis[f"Variación {nombre}"] = diferencia
                df_analisis[f"% variación {nombre}"] = porcentaje

            # Mostrar los resultados en orden cronológico.
            columnas_orden_final = (
                [nombre_dimension, nombre_dimension_secundaria]
                if hay_doble_agrupacion
                else [nombre_dimension]
            )

            df_analisis = df_analisis.sort_values(
                columnas_orden_final
            )

        # Preparar las columnas de la tabla.
        columnas_numericas = set(nombres_metricas.values())

        columnas_numericas.update(
            columna
            for columna in df_analisis.columns
            if columna.startswith("Variación ")
            or columna.startswith("% variación ")
        )

        columnas = [
            {
                "name": columna,
                "id": columna,
                "type": (
                    "numeric"
                    if columna in columnas_numericas
                    else "text"
                )
            }
            for columna in df_analisis.columns
        ]

        # Redondear los valores numéricos de la tabla a dos decimales.
        datos = df_analisis.round(2).to_dict("records")

        # Aplicar colores según el signo de las variaciones.
        estilos_condicionales = []

        for columna in df_analisis.columns:
            if (
                columna.startswith("Variación ")
                or columna.startswith("% variación ")
            ):
                estilos_condicionales.extend([
                    {
                        "if": {
                            "filter_query": f"{{{columna}}} > 0",
                            "column_id": columna
                        },
                        "color": "green",
                        "fontWeight": "bold"
                    },
                    {
                        "if": {
                            "filter_query": f"{{{columna}}} < 0",
                            "column_id": columna
                        },
                        "color": "red",
                        "fontWeight": "bold"
                    }
                ])

        # Seleccionar la primera métrica para el gráfico.
        nombre_metrica = nombres_metricas[metricas[0]]

        if nombre_metrica not in df_analisis.columns:
            figura = px.bar(
                title="No se encontró la métrica seleccionada"
            )
            figura.update_layout(template="plotly_white")
            return (
                columnas, datos, estilos_condicionales, figura
            )

        # Crear el gráfico utilizando los valores originales.
        if df_analisis.empty:
            figura = px.bar(
                title="No hay datos para los filtros seleccionados"
            )

        elif hay_doble_agrupacion:
            datos_grafico = df_analisis.copy()

            # Tratar la dimensión secundaria como categoría.
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
                hover_data=[
                    nombre_dimension,
                    nombre_dimension_secundaria
                ]
            )

        else:
            datos_grafico = df_analisis.copy()

            # Mantener el orden cronológico para las dimensiones temporales.
            if dimension in ("anio", "trimestre", "mes", "fecha"):
                datos_grafico = datos_grafico.sort_values(
                    nombre_dimension,
                    ascending=True
                )
            else:
                # Ordenar las categorías por la métrica, de menor a mayor.
                datos_grafico = datos_grafico.sort_values(
                    nombre_metrica,
                    ascending=True
                ).head(20)

            figura = px.bar(
                datos_grafico,
                x=nombre_dimension,
                y=nombre_metrica,
                title=nombre_metrica,
                hover_data=[nombre_dimension],
                category_orders={
                    nombre_dimension: (
                        datos_grafico[nombre_dimension]
                        .astype(str)
                        .tolist()
                    )
                }
            )

        figura.update_layout(
            template="plotly_white",
            margin={"l": 20, "r": 20, "t": 50, "b": 20},
            xaxis_title=nombre_dimension,
            yaxis_title=nombre_metrica
        )

        # Evitar valores intermedios en el eje X.
        figura.update_xaxes(type="category")

        return (
            columnas,
            datos,
            estilos_condicionales,
            figura
        )
