from sqlalchemy import create_engine, Column, Integer, VARCHAR, Sequence
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:admin@localhost:5432/rarity_db')
Base = declarative_base()


class Book(Base):
    __tablename__= 'Book'

    id = Column(Integer, Sequence('some_id,seq'), primary_key = True)
    name = Column,m                                                                                                                                                                                                                                                                                         cczz(VARCHAR(255), nullable = False)
    author = Column(VARCHAR(255), nullable = False)
    image = Column(VARCHAR(255))


Base.metadata.create_all(engine)