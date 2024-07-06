# TODO

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Configuration de la base de données
DATABASE_URL = 'postgresql://user:password@localhost/yourdatabase'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# Définition des tables
class Groupement(Base):
    __tablename__ = 'Groupement'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Gare(Base):
    __tablename__ = 'Gares'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    id_groupement = Column(Integer, ForeignKey('Groupement.id'))
    groupement = relationship(Groupement)


class Quai(Base):
    __tablename__ = 'Quais'
    id = Column(Integer, primary_key=True)
    id_gare = Column(Integer, ForeignKey('Gares.id'))
    ligne_quai = Column(String)
    type = Column(String)
    gare = relationship(Gare)


class Trajet(Base):
    __tablename__ = 'Trajet'
    id = Column(Integer, primary_key=True)
    id_train = Column(Integer, ForeignKey('Circulation.id'))
    id_quai_depart = Column(Integer, ForeignKey('Quais.id'))
    id_quai_arrivee = Column(Integer, ForeignKey('Quais.id'))
    h_depart = Column(DateTime)
    h_arrivee = Column(DateTime)
    trajet_time = Column(Integer)


class Circulation(Base):
    __tablename__ = 'Circulation'
    id = Column(Integer, primary_key=True)
    date_insertion = Column(DateTime, default=datetime.utcnow)
    id_train = Column(String, unique=True)


Base.metadata.create_all(engine)


# Fonction pour vérifier et insérer les gares
def check_and_insert_gares(gares):
    for gare_name in gares.set_gares:
        gare = session.query(Gare).filter_by(name=gare_name).first()
        if not gare:
            new_gare = Gare(name=gare_name)
            session.add(new_gare)
    session.commit()


# Fonction pour vérifier et insérer les quais
def check_and_insert_quais(circulations):
    for circulation in circulations.values():
        for stop in iter_stops(circulation.trajet.head):
            gare = session.query(Gare).filter_by(name=stop.name_gare).first()
            if gare:
                quai = session.query(Quai).filter_by(id_gare=gare.id, ligne_quai=circulation.quai,
                                                     type=circulation.circulation_type).first()
                if not quai:
                    new_quai = Quai(id_gare=gare.id, ligne_quai=circulation.quai, type=circulation.circulation_type)
                    session.add(new_quai)
    session.commit()


# Fonction pour itérer sur les arrêts d'un trajet
def iter_stops(head):
    current = head
    while current:
        yield current
        current = current.next_gare


# Fonction pour insérer les circulations
def insert_circulations(circulations):
    for circulation in circulations.values():
        if not session.query(Circulation).filter_by(id_train=circulation.id_circulation).first():
            new_circulation = Circulation(id_train=circulation.id_circulation)
            session.add(new_circulation)
    session.commit()


# Fonction pour insérer les trajets
def insert_trajets(circulations):
    for circulation in circulations.values():
        current_stop = circulation.trajet.head
        while current_stop and current_stop.next_gare:
            gare_depart = session.query(Gare).filter_by(name=current_stop.name_gare).first()
            gare_arrivee = session.query(Gare).filter_by(name=current_stop.next_gare.name_gare).first()
            quai_depart = session.query(Quai).filter_by(id_gare=gare_depart.id, ligne_quai=circulation.quai,
                                                        type=circulation.circulation_type).first()
            quai_arrivee = session.query(Quai).filter_by(id_gare=gare_arrivee.id, ligne_quai=circulation.quai,
                                                         type=circulation.circulation_type).first()

            new_trajet = Trajet(
                id_train=session.query(Circulation).filter_by(id_train=circulation.id_circulation).first().id,
                id_quai_depart=quai_depart.id,
                id_quai_arrivee=quai_arrivee.id,
                h_depart=datetime.strptime(current_stop.h_stop, '%Y%m%dT%H%M%S'),
                h_arrivee=datetime.strptime(current_stop.next_gare.h_stop, '%Y%m%dT%H%M%S')
            )
            session.add(new_trajet)
            current_stop = current_stop.next_gare
    session.commit()


# Exécution des fonctions
check_and_insert_gares(gares)
check_and_insert_quais(circulations)
insert_circulations(circulations)
insert_trajets(circulations)
