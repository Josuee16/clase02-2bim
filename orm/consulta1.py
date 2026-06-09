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
            .options(selectinload(Serie.actores))
            .order_by(Serie.titulo)
            .all()
        )

        for s in series:
            edades = [actor.edad for actor in s.actores if actor.edad is not None]
            promedio = sum(edades) / len(edades) if edades else None
            if promedio is not None:
                print(f"{s.titulo}: {promedio:.2f}")

if __name__ == '__main__':
    main()
