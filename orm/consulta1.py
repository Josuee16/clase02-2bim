"""
Obtener el titulo de la serie con el promedio de edad de los actores.
"""

from sqlalchemy.orm import Session, selectinload
from modelo import engine, Serie


def main():
    with Session(engine) as session:
        series = (
            session
            .query(Serie)
            .all()
        )

        for s in series:
            premios = s.obtener_premios()
            edad_promedio = s.obtener_edad_actores()
            if edad_promedio is not None:
                print(f"{s.titulo}: {edad_promedio:.2f} {premios}")
            else:
                print(f"{s.titulo}: No hay actores")

if __name__ == '__main__':
    main()
