import sqlite3
import random
from datetime import datetime

def seed_database():
    conn = sqlite3.connect('animalitos.db')
    c = conn.cursor()

    # --- Borrar datos existentes (opcional, si quieres empezar de cero cada vez) ---
    # c.execute('DELETE FROM especies')
    # conn.commit()
    # st.write("Datos existentes borrados.") # Esto solo si lo usas con Streamlit. Aquí no es necesario.

    # --- Datos de ejemplo ---
    especies_ejemplo = [
        {
            "nombre": "Panda Gigante",
            "nombre_cientifico": "Ailuropoda melanoleuca",
            "descripcion": "Un oso grande y distintivo, nativo de China, conocido por su pelaje blanco y negro.",
            "estado_conservacion": "Vulnerable",
            "estado_sugerido_uicn": "Vulnerable (Sugerido)",
            "poblacion_estimada": 1864,
            "tendencia_poblacion": "Creciendo",
            "amenazas": "Pérdida de hábitat, fragmentación, baja tasa de reproducción",
            "pais": "China",
            "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Giant_Panda_at_Washington_DC_Zoo.JPG" # Ejemplo de URL de imagen
        },
        {
            "nombre": "Tigre de Bengala",
            "nombre_cientifico": "Panthera tigris tigris",
            "descripcion": "El felino más grande del mundo, con distintivas rayas negras sobre pelaje naranja rojizo.",
            "estado_conservacion": "En Peligro",
            "estado_sugerido_uicn": "En Peligro (Sugerido)",
            "poblacion_estimada": 3900,
            "tendencia_poblacion": "Creciendo", # Ligero aumento
            "amenazas": "Caza furtiva, pérdida de hábitat, conflicto con humanos",
            "pais": "India, Bangladesh, Nepal, Bután",
            
        },
        {
            "nombre": "Rinoceronte Negro",
            "nombre_cientifico": "Diceros bicornis",
            "descripcion": "Grandes herbívoros nativos del este y sur de África, con dos cuernos distintivos.",
            "estado_conservacion": "En Peligro Crítico",
            "estado_sugerido_uicn": "En Peligro Crítico (Sugerido)",
            "poblacion_estimada": 5630, # Aunque en peligro crítico, la población ha aumentado en los últimos años
            "tendencia_poblacion": "Creciendo",
            "amenazas": "Caza furtiva por sus cuernos, pérdida de hábitat",
            "pais": "Sudáfrica, Namibia, Kenia, Zimbabue",
            
        },
        {
            "nombre": "Leopardo de las Nieves",
            "nombre_cientifico": "Panthera uncia",
            "descripcion": "Un felino grande, críptico, nativo de las regiones montañosas de Asia Central y del Sur.",
            "estado_conservacion": "Vulnerable",
            "estado_sugerido_uicn": "Vulnerable (Sugerido)",
            "poblacion_estimada": 4000,
            "tendencia_poblacion": "Decreciendo",
            "amenazas": "Caza furtiva, pérdida de presas, conflicto con ganadería",
            "pais": "China, Mongolia, India, Nepal, Pakistán, Rusia",
            
        },
        {
            "nombre": "Orangután de Borneo",
            "nombre_cientifico": "Pongo pygmaeus",
            "descripcion": "Uno de los grandes simios, endémico de la isla de Borneo, conocido por su inteligencia.",
            "estado_conservacion": "En Peligro Crítico",
            "estado_sugerido_uicn": "En Peligro Crítico (Sugerido)",
            "poblacion_estimada": 104700, # Gran número pero fuerte descenso
            "tendencia_poblacion": "Decreciendo",
            "amenazas": "Deforestación para aceite de palma, minería, incendios, caza ilegal",
            "pais": "Indonesia, Malasia",
            
        }
    ]

    # Insertar los datos si la tabla está vacía o si quieres rellenar siempre
    # Puedes comentar esta línea si solo quieres añadir una vez.
    # st.write(f"Insertando {len(especies_ejemplo)} especies de ejemplo...")
    
    for especie_data in especies_ejemplo:
        # Preparamos los datos para la inserción
        data_tuple = (
            especie_data['nombre'],
            especie_data['nombre_cientifico'],
            especie_data['descripcion'],
            especie_data['estado_conservacion'],
            especie_data['estado_sugerido_uicn'],
            especie_data['poblacion_estimada'],
            especie_data['tendencia_poblacion'],
            especie_data['amenazas'],
            especie_data['pais']
          
        )
        
        # Insertar los datos en la tabla. Usamos IGNORE para no insertar si ya existe por PRIMARY KEY,
        # pero aquí como no hay UNIQUE constraints en 'nombre', siempre insertará.
        # Una mejor forma para evitar duplicados sería primero buscar el nombre.
        c.execute('''
            INSERT INTO especies (
                nombre, nombre_cientifico, descripcion, estado_conservacion,
                estado_sugerido_uicn, poblacion_estimada, tendencia_poblacion,
                amenazas, pais
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data_tuple)
    
    conn.commit()
    conn.close()
    print("Base de datos sembrada con éxito con datos de ejemplo.")


if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando corres seed_db.py directamente
    # Primero nos aseguramos de que la base de datos y la tabla existan
    print("Asegurando que la base de datos esté lista...")
    # Puedes llamar a tu script crear_db.py aquí si quieres asegurarte
    # O simplemente tener la lógica de creación en este mismo archivo
    
    # Simple check for the table presence. If not, the seed will fail.
    # In a real app, you might import and run crear_db.py's function here.
    try:
        conn = sqlite3.connect('animalitos.db')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='especies';")
        if not c.fetchone():
            print("La tabla 'especies' no existe. Por favor, asegúrate de haber ejecutado 'crear_db.py' primero.")
            conn.close()
            exit() # Salimos si la tabla no existe
        conn.close()
        
        seed_database()
    except sqlite3.OperationalError as e:
        print(f"Error al conectar o interactuar con la base de datos: {e}")
        print("Asegúrate de que el archivo 'animalitos.db' no esté bloqueado o que la carpeta sea accesible.")