from pathlib import Path
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import cadena_base_datos
from modelo import Base, engine, Pais

engine = create_engine(cadena_base_datos)
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'

# Leemos el CSV y cargamos los datos de países a la base de datos
def load_csv(filename):
    with open(DATA_DIR / filename, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

# Creamos el esquema de la base de datos y luego cargamos los datos desde el CSV
def main():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        count = 0
        for filename in ('paises.csv',):
            for row in load_csv(filename):
                pais = Pais(
                    id=int(row['id']),
                    nombre=row['nombre'].strip(),
                    continente=row.get('continente', '').strip() or None,
                )
                session.merge(pais)
                count += 1
        session.commit()
    print(f'Paises cargados/actualizados: {count}')

# Ejecutamos la función principal para cargar los datos
if __name__ == '__main__':
    main()
