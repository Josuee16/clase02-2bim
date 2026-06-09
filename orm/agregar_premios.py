from pathlib import Path
import csv
from sqlalchemy.orm import Session
from config import cadena_base_datos
from modelo import Base, Serie, Premio
from sqlalchemy import create_engine


engine = create_engine(cadena_base_datos)
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'

# Función para cargar datos desde un archivo CSV
def load_csv(filename):
    with open(DATA_DIR / filename, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

# Función para convertir un valor a entero o devolver None si está vacío
def int_or_none(value):
    return int(value) if value and value.strip() else None

# Creamos el esquema de la base de datos y luego cargamos los datos desde el CSV
def main():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        count = 0
        for row in load_csv('premios.csv'):
            serie = session.query(Serie).filter_by(titulo=row['serie'].strip()).one()
            premio = Premio(
                id=int(row['id']),
                nombre_premio=row['nombre_premio'].strip(),
                categoria=row.get('categoria', '').strip() or None,
                anio=int_or_none(row.get('anio', '')),
                serie_id=serie.id,
            )
            session.merge(premio)
            count += 1
        session.commit()
    print(f'Premios cargados/actualizados: {count}')

# Ejecutamos la función principal para cargar los datos
if __name__ == '__main__':
    main()
