from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func, UniqueConstraint

from db.base import Base, inverse_relationship, create_tables 


# add your models here

class User(Base):
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Movie(Base):

    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)

    api_id = Column(Integer, unique=True)
    url = Column(String, unique=True)
    name = Column(String)
    image = Column(String)

    def parse_json(self, data):
        self.api_id = data['show']['id']
        self.url = data['show']['url']
        self.name = data['show']['name']
        try:
            self.image = data['show']['image']['medium']
        except:
            self.image = None

class Like(Base):

    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref=inverse_relationship('users'))

    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship(Movie, backref=inverse_relationship('movies'))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


if __name__ != '__main__':
    create_tables()