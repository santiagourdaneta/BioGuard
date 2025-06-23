# 🌱 BioGuard: Plataforma de Conservación de Especies con IA y Gestión de Datos 🐅

https://github.com/santiagourdaneta/BioGuard/blob/main/screenshot1.png
https://github.com/santiagourdaneta/BioGuard/blob/main/screenshot2.png
https://github.com/santiagourdaneta/BioGuard/blob/main/screenshot3.png
https://github.com/santiagourdaneta/BioGuard/blob/main/screenshot4.png

## Descripción del Proyecto

BioGuard es una **plataforma interactiva construida con Streamlit y SQLite** diseñada para biólogos, conservacionistas y entusiastas de la vida silvestre. Permite una gestión eficiente de datos de especies, incorporando **funcionalidades de Inteligencia Artificial (IA)** para sugerir estados de conservación y análisis de tendencias.

Con BioGuard, puedes:

* **Registrar nuevas especies** con detalles ecológicos y de conservación.
* **Explorar y buscar especies** existentes con filtros avanzados por estado de conservación, país y tendencia poblacional.
* **Eliminar** registros de especies fácilmente.
* **Cargar datos masivos** de especies desde archivos CSV, facilitando la importación de grandes conjuntos de información.
* Visualizar **análisis y estadísticas clave** sobre la distribución y las amenazas de las especies mediante gráficos interactivos.
* Beneficiarte de una **sugerencia automática de estado de conservación UICN** basada en datos poblacionales y amenazas.

BioGuard se presenta como una herramienta robusta y amigable para la **conservación de la biodiversidad** y el **monitoreo de especies en riesgo**, facilitando la toma de decisiones informadas en el ámbito de la ecología y la sostenibilidad.

## Características Destacadas

* **Interfaz Intuitiva con Streamlit**: Rápida prototipado y despliegue de dashboards interactivos.
* **Base de Datos SQLite**: Almacenamiento ligero y eficiente para la gestión de especies.
* **Importación de Datos CSV**: Carga masiva de información para poblar la base de datos.
* **Filtros y Búsqueda Avanzados**: Encuentra fácilmente la información que necesitas.
* **Análisis y Visualización de Datos**: Gráficos interactivos con `Plotly Express`.
* **Integración de IA (Sugerencia UICN)**: Lógica basada en reglas para la clasificación del estado de conservación.
* **Código Limpio y Modular**: Fácil de entender, mantener y extender.

## Cómo Usar y Ejecutar el Proyecto

### Requisitos

Asegúrate de tener Python 3.8+ instalado.

### Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/santiagourdaneta/BioGuard/
    cd BioGuard
    ```
2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```
3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### Ejecución

1.  **Crea la base de datos y la tabla:**
    ```bash
    python crear_db.py
    ```
2.  **(Opcional) Siembra la base de datos con datos de ejemplo:**
    ```bash
    python seed_db.py
    ```
    O usa la funcionalidad "Cargar Datos (CSV)" en la interfaz de usuario para importar datos.

3.  **Inicia la aplicación Streamlit:**
    ```bash
    streamlit run app.py
    ```
    La aplicación se abrirá automáticamente en tu navegador web.

## Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar BioGuard, no dudes en abrir un *issue* o enviar un *pull request*.

## Contacto

¿Preguntas o comentarios? Conéctate con [Santiago Urdaneta](https://github.com/santiagourdaneta/).
