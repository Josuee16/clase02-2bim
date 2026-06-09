from pathlib import Path
import csv
from sqlalchemy.orm import Session
from modelo import Base, Pais, Plataforma
from sqlalchemy import create_engine
from config import cadena_base_datos


engine = create_engine(cadena_base_datos)

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'

# Cargamos los datos de plataformas desde el CSV a la base de datos
def load_csv(filename):
    with open(DATA_DIR / filename, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

# Creamos el esquema de la base de datos y luego cargamos los datos desde el CSV
def main():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        count = 0
        for row in load_csv('plataformas.csv'):
            pais = session.query(Pais).filter_by(nombre=row['pais'].strip()).one()
            plataforma = Plataforma(
                id=int(row['id']),
                nombre=row['nombre'].strip(),
                pais_id=pais.id,
                suscriptores_millones=float(row['suscriptores_millones']) if row['suscriptores_millones'].strip() else None,
            )
            session.merge(plataforma)
            count += 1
        session.commit()
    print(f'Plataformas cargadas/actualizadas: {count}')

# Ejecutamos la función principal para cargar los datos
if __name__ == '__main__':
    main()
