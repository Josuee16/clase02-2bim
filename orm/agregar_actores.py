from pathlib import Path
import csv
from sqlalchemy.orm import Session
from config import cadena_base_datos
from sqlalchemy import create_engine
from modelo import Base, Pais, Serie, Actor

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
        for filename in ('actores.csv',):
            for row in load_csv(filename):
                pais_nombre = row['pais'].strip()
                serie_titulo = row['serie'].strip()

                pais = session.query(Pais).filter_by(nombre=pais_nombre).one_or_none()
                if pais is None:
                    raise ValueError(
                        f"No se encontró el país '{pais_nombre}' para actor id={row.get('id')} nombre={row.get('nombre')}"
                    )

                serie = session.query(Serie).filter_by(titulo=serie_titulo).one_or_none()
                if serie is None:
                    raise ValueError(
                        f"No se encontró la serie '{serie_titulo}' para actor id={row.get('id')} nombre={row.get('nombre')}"
                    )

                actor = Actor(
                    id=int(row['id']),
                    nombre=row['nombre'].strip(),
                    edad=int_or_none(row.get('edad', '')),
                    rol=row.get('rol', '').strip() or None,
                    pais_id=pais.id,
                    serie_id=serie.id,
                )
                session.merge(actor)
                count += 1
        session.commit()
    print(f'Actores cargados/actualizados: {count}')

# Ejecutamos la función principal para cargar los datos
if __name__ == '__main__':
    main()
