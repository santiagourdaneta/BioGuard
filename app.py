import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np
import io # Necesario para leer archivos subidos

# --- Funciones de Conexión a la Base de Datos ---
def get_db_connection():
    conn = sqlite3.connect('animalitos.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Lógica de IA Simplificada (Clasificación Automática UICN) ---
# Esto simula un algoritmo basado en reglas para la clasificación UICN
def clasificar_uicn(poblacion, tendencia, amenazas_str, paises_str):
    # Reglas simplificadas (¡Un modelo real de la UICN es mucho más complejo!)
    if poblacion is None: # Manejar caso donde poblacion es nula
        poblacion = 0
    if poblacion < 500 and "caza" in amenazas_str.lower() and tendencia == "Decreciendo":
        return "En Peligro Crítico (Sugerido)"
    elif poblacion < 2500 and tendencia == "Decreciendo":
        return "En Peligro (Sugerido)"
    elif poblacion < 10000 and "deforestacion" in amenazas_str.lower():
        return "Vulnerable (Sugerido)"
    else:
        return "Preocupación Menor (Sugerido)"


# --- Configuración de la Página y Título ---
st.set_page_config(layout="wide", page_title="BioGuard - Sistema de Clasificación de Especies")
st.title("🌱 BioGuard: Plataforma para la Conservación de Especies 🐅")
st.markdown("Una herramienta avanzada para biólogos, conservacionistas y desarrolladores de software ambiental.")

# --- Barra lateral para Navegación ---
st.sidebar.title("Menú Principal")
page_selection = st.sidebar.radio("Navegar", ["Añadir Especie", "Explorar Especies", "Análisis y Predicción", "Cargar Datos (CSV)"])

# --- Sección para Añadir una Nueva Especie ---
if page_selection == "Añadir Especie":
    st.header("➕ Registrar Nueva Especie y Clasificar")
    with st.form("agregar_animal_form"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre Común:", key="add_nombre")
            nombre_cientifico = st.text_input("Nombre Científico:", key="add_nombre_cientifico")
            descripcion = st.text_area("Descripción de la Especie:", key="add_desc")
            # --- CAMBIO AQUÍ: input de texto para múltiples países ---
            paises_str = st.text_input("Países donde habita (separar por comas, ej: Perú, Ecuador, Brasil):", key="add_paises")
            
        with col2:
            st.subheader("Datos Ecológicos y de Conservación")
            poblacion_estimada = st.number_input("Población Estimada (ej. 1000):", min_value=0, value=0, key="add_poblacion")
            tendencia_poblacion_options = ["Decreciendo", "Estable", "Creciendo", "Desconocida"]
            tendencia_poblacion = st.selectbox("Tendencia de la Población:", tendencia_poblacion_options, key="add_tendencia")
            amenazas = st.text_area("Principales Amenazas (separar por comas):", key="add_amenazas")
            
            # Clasificación automática UICN
            st.markdown("---")
            st.markdown("**Sugerencia de Clasificación UICN (Automático):**")
            # Pasamos la cadena de países al clasificador para una posible mejora de IA
            estado_uicn_sugerido = clasificar_uicn(poblacion_estimada, tendencia_poblacion, amenazas, paises_str)
            st.info(estado_uicn_sugerido)
            
            estado_conservacion_options = ["En Peligro Crítico", "En Peligro", "Vulnerable", "Casi Amenazado", "Preocupación Menor", "Datos Insuficientes", "No Evaluado"]
            estado_conservacion_manual = st.selectbox("Estado de Conservación (Manual - Según Criterios UICN):", estado_conservacion_options, key="add_estado_manual")

        submitted = st.form_submit_button("Guardar Especie")

        if submitted:
            if nombre and estado_conservacion_manual:
                conn = get_db_connection()
                conn.execute('INSERT INTO especies (nombre, nombre_cientifico, descripcion, estado_conservacion, estado_sugerido_uicn, poblacion_estimada, tendencia_poblacion, amenazas, pais) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                             (nombre, nombre_cientifico, descripcion, estado_conservacion_manual, estado_uicn_sugerido, poblacion_estimada, tendencia_poblacion, amenazas, paises_str)) # Guardamos la cadena de países
                conn.commit()
                conn.close()
                st.success(f"¡'{nombre}' ha sido registrado!")
                st.rerun() # Recargar para ver el cambio
            else:
                st.error("Por favor, llena al menos el Nombre Común y el Estado de Conservación Manual.")

# --- Sección de Exploración de Especies (Búsqueda, Filtros, Orden, Paginación) ---
elif page_selection == "Explorar Especies":
    st.header("🔎 Enciclopedia de Especies por Conservar")

    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        search_query = st.text_input("Buscar por Nombre Común o Científico:", "").lower()
    with col_filter2:
        estados_conservacion_filtro = ["Todos"] + ["En Peligro Crítico", "En Peligro", "Vulnerable", "Casi Amenazado", "Preocupación Menor", "Datos Insuficientes", "No Evaluado"]
        selected_estado_filtro = st.selectbox("Filtrar por Estado:", estados_conservacion_filtro)
    
    # --- CAMBIO AQUÍ: multiselect para varios países ---
    conn = get_db_connection()
    # Obtenemos todos los países únicos que aparecen en la base de datos (incluso si están en una cadena)
    all_paises_raw = conn.execute('SELECT DISTINCT pais FROM especies WHERE pais IS NOT NULL').fetchall()
    conn.close()
    
    # Procesar la cadena de países para obtener una lista única de todos los países mencionados
    unique_paises = set()
    for row in all_paises_raw:
        if row['pais']:
            for p in row['pais'].split(','):
                unique_paises.add(p.strip())
    
    paises_lista_filtro = sorted(list(unique_paises))
    selected_paises_filtro = st.multiselect("Filtrar por País/Países (selecciona uno o más):", paises_lista_filtro)

    sort_by = st.selectbox("Ordenar por:", ["Nombre (A-Z)", "Nombre (Z-A)", "Estado de Conservación (Más Crítico Primero)", "Población (Menor a Mayor)"])

    conn = get_db_connection()
    all_especies_raw = conn.execute('SELECT * FROM especies').fetchall()
    conn.close()

    # Definimos explícitamente los nombres de las columnas en el orden correcto
    # Asegúrate de que este orden coincida con el orden en crear_db.py
    column_names = [
        'id', 'nombre', 'nombre_cientifico', 'descripcion', 
        'estado_conservacion', 'estado_sugerido_uicn', 'poblacion_estimada', 
        'tendencia_poblacion', 'amenazas', 'pais'
    ]
    df_especies = pd.DataFrame(all_especies_raw, columns=column_names)

    # --- CÓDIGO DE DIAGNÓSTICO (mantenerlo por ahora) ---
 #   st.write(f"DataFrame vacío: {df_especies.empty}")
 #   st.write(f"Columnas del DataFrame: {df_especies.columns.tolist()}")
    # --- FIN DE CÓDIGO DE DIAGNÓSTICO ---

    # Aplicar filtros
    if not df_especies.empty:
        # Búsqueda por nombre común o científico
        filtered_df = df_especies[
            df_especies['nombre'].str.lower().str.contains(search_query, na=False) |
            df_especies['nombre_cientifico'].str.lower().str.contains(search_query, na=False)
        ]
        
        if selected_estado_filtro != "Todos":
            filtered_df = filtered_df[filtered_df['estado_conservacion'] == selected_estado_filtro]
        
        # --- CAMBIO AQUÍ: Filtrado para múltiples países ---
        if selected_paises_filtro: # Si se seleccionó al menos un país
            # Filtramos si la columna 'pais' contiene AL MENOS UNO de los países seleccionados
            filtered_df = filtered_df[
                filtered_df['pais'].astype(str).apply(
                    lambda x: any(p.strip() in [country.strip() for country in x.split(',')] for p in selected_paises_filtro)
                )
            ]


        # Ordenar
        if sort_by == "Nombre (A-Z)":
            filtered_df = filtered_df.sort_values(by='nombre', ascending=True)
        elif sort_by == "Nombre (Z-A)":
            filtered_df = filtered_df.sort_values(by='nombre', ascending=False)
        elif sort_by == "Estado de Conservación (Más Crítico Primero)":
            orden_estados = {"En Peligro Crítico": 1, "En Peligro": 2, "Vulnerable": 3, 
                             "Casi Amenazado": 4, "Preocupación Menor": 5, 
                             "Datos Insuficientes": 6, "No Evaluado": 7}
            # Usar .map y luego sort_values
            filtered_df['orden_estado'] = filtered_df['estado_conservacion'].map(orden_estados)
            # Asegurarse de que los valores NaN de orden_estado vayan al final o se manejen
            filtered_df = filtered_df.sort_values(by='orden_estado', na_position='last').drop(columns='orden_estado')
        elif sort_by == "Población (Menor a Mayor)":
            # Asegurarse de que 'poblacion_estimada' sea numérica y manejar NaN
            filtered_df['poblacion_estimada'] = pd.to_numeric(filtered_df['poblacion_estimada'], errors='coerce')
            filtered_df = filtered_df.sort_values(by='poblacion_estimada', ascending=True, na_position='last')
        # --- Botón de Exportar a CSV ---
        if not filtered_df.empty:
                    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Exportar Especies a CSV",
                        data=csv_data,
                        file_name="especies_bioguard.csv",
                        mime="text/csv",
                        help="Descarga el listado actual de especies con los filtros aplicados."
                    )
                    st.markdown("---") # Separador para que se vea limpio

        # Paginación
        items_per_page = 5
        total_pages = (len(filtered_df) + items_per_page - 1) // items_per_page
        if total_pages == 0: total_pages = 1 # Para evitar error si no hay elementos
        current_page = st.number_input("Página:", 1, total_pages, key="pagination_browse")

        start_index = (current_page - 1) * items_per_page
        end_index = start_index + items_per_page
        displayed_especies = filtered_df.iloc[start_index:end_index]
        # --- Visualización de Especies con Botones de Edición/Eliminación ---
        if not displayed_especies.empty:
            for index, especie in displayed_especies.iterrows():
                st.markdown(f"### **{especie['nombre']}** ({especie['nombre_cientifico'] or 'N/A'})")
                st.write(f"**Estado de Conservación (UICN):** :red[{especie['estado_conservacion']}]" if especie['estado_conservacion'] in ["En Peligro Crítico", "En Peligro", "Vulnerable"] else f"**Estado de Conservación (UICN):** {especie['estado_conservacion']}")
                st.write(f"**Sugerencia AI:** {especie['estado_sugerido_uicn']}")
                st.write(f"**Población Estimada:** {especie['poblacion_estimada']} individuos")
                st.write(f"**Tendencia Poblacional:** {especie['tendencia_poblacion']}")
                st.write(f"**Países:** {especie['pais']}") # Muestra la cadena de países
                st.write(f"**Descripción:** {especie['descripcion']}")
                st.write(f"**Principales Amenazas:** {especie['amenazas']}")
               
                col_actions = st.columns(1)
                
                with col_actions[0]:
                    if st.button(f"🗑️ Eliminar {especie['nombre']}", key=f"delete_{especie['id']}"):
                        conn = get_db_connection()
                        conn.execute("DELETE FROM especies WHERE id = ?", (especie['id'],))
                        conn.commit()
                        conn.close()
                        st.success(f"Especie '{especie['nombre']}' eliminada.")
                        st.rerun()
                st.markdown("---")       
        else:
            st.info("No se encontraron especies con los filtros aplicados.")
    else:
        st.info("Aún no hay especies registradas. ¡Añade una!")

# --- Sección de Análisis y Predicción (Ciencia de Datos y Estadísticas) ---
elif page_selection == "Análisis y Predicción":
    st.header("📈 Análisis de Datos Ecológicos y Modelos Predictivos")

    conn = get_db_connection()
    all_especies_analysis = conn.execute('SELECT * FROM especies').fetchall()
    conn.close()

    if all_especies_analysis:
        # Definimos explícitamente los nombres de las columnas para el análisis
        column_names_analysis = [
                'id', 'nombre', 'nombre_cientifico', 'descripcion', 
                'estado_conservacion', 'estado_sugerido_uicn', 'poblacion_estimada', 
                'tendencia_poblacion', 'amenazas', 'pais'
            ]
        df_analysis = pd.DataFrame(all_especies_analysis, columns=column_names_analysis)

            # --- CÓDIGO DE DIAGNÓSTICO (opcional aquí, pero puedes agregarlo si quieres confirmar) ---
            # st.write(f"Análisis DataFrame vacío: {df_analysis.empty}")
            # st.write(f"Análisis Columnas del DataFrame: {df_analysis.columns.tolist()}")
            # --- FIN CÓDIGO DE DIAGNÓSTICO ---
        
        st.subheader("1. Distribución por Estado de Conservación")
        estado_counts = df_analysis['estado_conservacion'].value_counts().reset_index()
        estado_counts.columns = ['Estado de Conservación', 'Número de Especies']
        fig_estado = px.bar(estado_counts, x='Estado de Conservación', y='Número de Especies',
                            color='Estado de Conservación',
                            title='Número de Especies por Estado de Conservación',
                            labels={'Estado de Conservación': 'Estado', 'Número de Especies': 'Cantidad'})
        st.plotly_chart(fig_estado, use_container_width=True)

        st.subheader("2. Tendencia Poblacional por Estado de Conservación")
        df_analysis_filtered = df_analysis.dropna(subset=['tendencia_poblacion'])
        if not df_analysis_filtered.empty:
            tendencia_estado_counts = df_analysis_filtered.groupby(['tendencia_poblacion', 'estado_conservacion']).size().reset_index(name='Count')
            fig_tendencia_estado = px.bar(tendencia_estado_counts, x='tendencia_poblacion', y='Count',
                                          color='estado_conservacion', barmode='group',
                                          title='Relación entre Tendencia Poblacional y Estado de Conservación')
            st.plotly_chart(fig_tendencia_estado, use_container_width=True)
        else:
            st.info("No hay datos de tendencia poblacional para analizar.")

        st.subheader("3. Análisis de Amenazas Comunes (Simulado)")
        amenazas_list = df_analysis['amenazas'].dropna().str.lower().str.split(', ').explode().tolist()
        if amenazas_list:
            amenazas_df = pd.DataFrame(amenazas_list, columns=['Amenaza'])
            amenaza_counts = amenazas_df['Amenaza'].value_counts().head(5).reset_index()
            amenaza_counts.columns = ['Amenaza', 'Frecuencia']
            fig_amenazas = px.pie(amenaza_counts, values='Frecuencia', names='Amenaza',
                                  title='Top 5 Amenazas Más Comunes')
            st.plotly_chart(fig_amenazas, use_container_width=True)
        else:
            st.info("No hay datos de amenazas para analizar.")

        st.subheader("4. Modelo Predictivo (Simulación de Riesgo Futuro)")
        st.info("Esta sección simula un modelo predictivo. En un sistema real, usaríamos algoritmos de Machine Learning (ej. Regresión Logística, Random Forest) entrenados con datos históricos de poblaciones y amenazas para predecir la probabilidad de cambio en el estado de conservación.")
        
        if not df_analysis.empty:
            df_analysis['riesgo_futuro_simulado'] = df_analysis.apply(lambda row: "Alto" if pd.notna(row['poblacion_estimada']) and row['poblacion_estimada'] < 1000 and row['tendencia_poblacion'] == 'Decreciendo' else "Bajo", axis=1)
            riesgo_counts = df_analysis['riesgo_futuro_simulado'].value_counts().reset_index()
            riesgo_counts.columns = ['Riesgo', 'Número de Especies']
            fig_riesgo = px.bar(riesgo_counts, x='Riesgo', y='Número de Especies',
                                color='Riesgo', title='Riesgo Futuro de Conservación (Simulado)')
            st.plotly_chart(fig_riesgo, use_container_width=True)
        else:
            st.info("No hay suficientes datos para la simulación predictiva.")

    else:
        st.info("No hay suficientes datos para realizar análisis y predicciones. ¡Por favor, añade algunas especies!")

        # --- NUEVA SECCIÓN: Cargar Datos desde CSV ---
elif page_selection == "Cargar Datos (CSV)":
            st.header("⬆️ Cargar Datos de Especies desde Archivo CSV")
            st.markdown("Sube un archivo CSV con tus datos de especies. Las columnas deben coincidir con las de la base de datos (ej. `nombre`, `nombre_cientifico`, `estado_conservacion`, `poblacion_estimada`, etc.).")

            uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

            if uploaded_file is not None:
                try:
                    # Leer el archivo CSV en un DataFrame de Pandas
                    df_uploaded = pd.read_csv(uploaded_file)
                    st.write("Vista previa de los datos cargados:")
                    st.dataframe(df_uploaded.head())

                    # Validaciones básicas de seguridad y estructura
                    required_columns = [
                        'nombre', 'nombre_cientifico', 'descripcion', 'estado_conservacion', 
                        'estado_sugerido_uicn', 'poblacion_estimada', 'tendencia_poblacion', 
                        'amenazas', 'pais' 
                    ]
                    
                    # Convertir todos los nombres de columna a minúsculas para una validación sin distinción de mayúsculas
                    df_uploaded.columns = df_uploaded.columns.str.lower()
                    
                    missing_columns = [col for col in required_columns if col not in df_uploaded.columns]

                    if missing_columns:
                        st.error(f"¡Error! Faltan las siguientes columnas requeridas en tu archivo CSV: {', '.join(missing_columns)}. Por favor, revisa el formato.")
                    else:
                        st.success("El archivo CSV parece tener las columnas correctas. ¡Listo para importar!")
                        
                        if st.button("Importar Datos a la Base de Datos"):
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            
                            rows_inserted = 0
                            rows_skipped = 0

                            for index, row in df_uploaded.iterrows():
                                # Preparar los datos para la inserción, asegurando el orden y manejando nulos
                                try:
                                    # Asegurarse de que todos los valores son cadenas o None
                                    # Usar .get(col, None) para manejar columnas que no estén presentes en el CSV pero sí en la DB
                                    data_to_insert = (
                                        str(row.get('nombre', '')),
                                        str(row.get('nombre_cientifico', '')),
                                        str(row.get('descripcion', '')),
                                        str(row.get('estado_conservacion', '')),
                                        str(row.get('estado_sugerido_uicn', clasificar_uicn(row.get('poblacion_estimada'), row.get('tendencia_poblacion'), row.get('amenazas'), row.get('pais')))), # Re-clasificar si no viene sugerido
                                        int(row.get('poblacion_estimada', 0)) if pd.notna(row.get('poblacion_estimada')) else 0, # Convertir a int, manejar NaN
                                        str(row.get('tendencia_poblacion', 'Desconocida')),
                                        str(row.get('amenazas', '')),
                                        str(row.get('pais', ''))
                                        
                                    )
                                    cursor.execute('''
                                        INSERT INTO especies (
                                            nombre, nombre_cientifico, descripcion, estado_conservacion,
                                            estado_sugerido_uicn, poblacion_estimada, tendencia_poblacion,
                                            amenazas, pais
                                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    ''', data_to_insert)
                                    rows_inserted += 1
                                except Exception as e:
                                    st.warning(f"Error al procesar la fila {index+1} ({row.get('nombre', 'N/A')}): {e}. Fila omitida.")
                                    rows_skipped += 1
                            
                            conn.commit()
                            conn.close()
                            st.success(f"¡Importación completada! Se insertaron {rows_inserted} especies y se omitieron {rows_skipped}.")
                            st.rerun()

                except pd.errors.EmptyDataError:
                    st.error("El archivo CSV está vacío.")
                except pd.errors.ParserError:
                    st.error("No se pudo analizar el archivo CSV. Asegúrate de que está bien formado.")
                except Exception as e:
                    st.error(f"Ocurrió un error inesperado al leer el archivo: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("Desarrollado con pasión por la conservación por [Santiago Urdaneta](http://github.com/santiagourdaneta/)")