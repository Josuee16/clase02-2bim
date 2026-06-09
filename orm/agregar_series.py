from pathlib import Path
import csv
from sqlalchemy.orm import Session
from modelo import Base, engine, Pais, Plataforma, Serie
from sqlalchemy import create_engine
from config import cadena_base_datos


engine = create_engine(cadena_base_datos)
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'

# Cargamos los datos de series desde el CSV a la base de datos
def load_csv(filename):
    with open(DATA_DIR / filename, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def int_or_none(value):
    return int(value) if value and value.strip() else None

# Creamos el esquema de la base de datos y luego cargamos los datos desde el CSV
def main():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        
        existing = {s.titulo: s for s in session.query(Serie).all()}

        created = {}

        count = 0
        for row in load_csv('series.csv',):
            titulo = row['titulo'].strip()
            pais = session.query(Pais).filter_by(nombre=row['pais'].strip()).one()
            plataforma = session.query(Plataforma).filter_by(nombre=row['plataforma'].strip()).one()

            if titulo in existing:
                s = existing[titulo]
                s.genero = row.get('genero', '').strip() or None
                s.anio_estreno = int_or_none(row.get('anio_estreno', ''))
                s.temporadas = int_or_none(row.get('temporadas', ''))
                s.plataforma_id = plataforma.id
                s.pais_id = pais.id
                session.add(s)
            elif titulo in created:
                s = created[titulo]
                s.genero = row.get('genero', '').strip() or None
                s.anio_estreno = int_or_none(row.get('anio_estreno', ''))
                s.temporadas = int_or_none(row.get('temporadas', ''))
                s.plataforma_id = plataforma.id
                s.pais_id = pais.id
            else:
             
                s = Serie(
                    titulo=titulo,
                    genero=row.get('genero', '').strip() or None,
                    anio_estreno=int_or_none(row.get('anio_estreno', '')),
                    temporadas=int_or_none(row.get('temporadas', '')),
                    plataforma_id=plataforma.id,
                    pais_id=pais.id,
                )
                session.add(s)
                created[titulo] = s

            count += 1

        session.commit()

    print(f'Series cargadas/actualizadas: {count}')

# Ejecutamos la función principal para cargar los datos
if __name__ == '__main__':
    main()
