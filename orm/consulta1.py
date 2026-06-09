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
            cantidad_premios = s.obtener_cantidad_premios()
            edad_promedio = s.obtener_edad_actores()

            if edad_promedio is not None:
                print(
                    f"Nombre de la Serie: {s.titulo} | "
                    f"Edad promedio de actores: {edad_promedio:.2f} | "
                    f"Cantidad de Premios ganados: {cantidad_premios}"
                )

if __name__ == '__main__':
    main()
