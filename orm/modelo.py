from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine

from config import cadena_base_datos

engine = create_engine(cadena_base_datos)

Base = declarative_base()

class Pais(Base):
    __tablename__ = 'pais'
    id         = Column(Integer, primary_key=True, autoincrement=True)
    nombre     = Column(String(100), unique=True, nullable=False)
    continente = Column(String(100), nullable=False)

    plataformas = relationship('Plataforma', back_populates='pais')
    series      = relationship('Serie',      back_populates='pais')
    actores     = relationship('Actor',      back_populates='pais')

    def __repr__(self):
        return f"Pais: {self.nombre}"


class Plataforma(Base):
    __tablename__ = 'plataforma'
    id                    = Column(Integer, primary_key=True, autoincrement=True)
    nombre                = Column(String(100), unique=True, nullable=False)
    pais_id               = Column(Integer, ForeignKey('pais.id'), nullable=True)
    suscriptores_millones = Column(Integer)

    pais   = relationship('Pais',  back_populates='plataformas')
    series = relationship('Serie', back_populates='plataforma')

    def __repr__(self):
        return f"Plataforma: {self.nombre}"


class Serie(Base):
    __tablename__ = 'serie'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    titulo        = Column(String(200), nullable=False)
    genero        = Column(String(100))
    anio_estreno  = Column(Integer)
    temporadas    = Column(Integer)
    plataforma_id = Column(Integer, ForeignKey('plataforma.id'))
    pais_id       = Column(Integer, ForeignKey('pais.id'))

    plataforma = relationship('Plataforma', back_populates='series')
    pais       = relationship('Pais',       back_populates='series')
    actores    = relationship('Actor',      back_populates='serie')
    premios    = relationship('Premio',     back_populates='serie')

    def __repr__(self):
        return f"Serie: {self.titulo}"
    
    def obtener_edad_actores(self):
        edades = [e.edad for e in self.actores if e.edad is not None]
        if edades:
            return sum(edades) / len(edades)
        return 0.0

    def obtener_premios(self):
        return [p.nombre_premio for p in self.premios]

class Actor(Base):
    __tablename__ = 'actor'
    id       = Column(Integer, primary_key=True, autoincrement=True)
    nombre   = Column(String(200), nullable=False)
    edad     = Column(Integer)
    rol      = Column(String(100))
    pais_id  = Column(Integer, ForeignKey('pais.id'))
    serie_id = Column(Integer, ForeignKey('serie.id'))

    pais  = relationship('Pais',  back_populates='actores')
    serie = relationship('Serie', back_populates='actores')

    def __repr__(self):
        return f"Actor: {self.nombre}"


class Premio(Base):
    __tablename__ = 'premio'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    nombre_premio = Column(String(200), nullable=False)
    categoria     = Column(String(100))
    anio          = Column(Integer)
    serie_id      = Column(Integer, ForeignKey('serie.id'))

    serie = relationship('Serie', back_populates='premios')

    def __repr__(self):
        return f"Premio: {self.nombre_premio}"

Base.metadata.create_all(engine)
