import sqlite3

conn = sqlite3.connect('animalitos.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS especies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        nombre_cientifico TEXT,
        descripcion TEXT,
        estado_conservacion TEXT NOT NULL,
        estado_sugerido_uicn TEXT,
        poblacion_estimada INTEGER,
        tendencia_poblacion TEXT,
        amenazas TEXT,
        pais TEXT
    )
''')
conn.commit()
conn.close()