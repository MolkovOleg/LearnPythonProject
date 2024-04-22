from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from source.db.db import Base, engine


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)

    feedbacks = relationship('FeedbackUser')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User id: {self.id}, name: {self.first_name}'


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    apartments = relationship('Apartment', back_populates='city')


class Area(Base):
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    apartments = relationship('Apartment', back_populates='area')


class RoomCount(Base):
    __tablename__ = 'room_counts'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    apartments = relationship('Apartment', back_populates='rooms_count')


class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    address = Column(String)
    city_id = Column(Integer, ForeignKey("cities.id"))
    area_id = Column(Integer, ForeignKey("areas.id"))
    owner_name = Column(String)
    rooms_id = Column(Integer, ForeignKey('room_counts.id'))
    photos = Column(String)
    website = Column(String)

    feedbacks = relationship('Feedback', lazy='joined')
    city = relationship('City', back_populates='apartments')
    area = relationship('Area', back_populates='apartments')
    rooms_count = relationship('RoomCount', back_populates='apartments')

    def __repr__(self):
        return f'Apartament id: {self.id}, name: {self.address}'


class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey(Apartment.id), index=True, nullable=False)
    raiting = Column(Integer)
    price = Column(Integer)
    owner_name = Column(String)
    text = Column(String)
    photo = Column(String)

    apartments = relationship('Apartment', lazy='joined')
    feedbacks = relationship('FeedbackUser')

    def __repr__(self):
        return f'Feedback id: {self.id}, raiting: {self.raiting}'


class FeedbackUser(Base):
    __tablename__ = 'feedbacks_user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    feedback_id = Column(Integer, ForeignKey(Feedback.id), index=True, nullable=False)
    publication_date = Column(Date)

    users = relationship('User', lazy='joined')
    feedbacks = relationship('Feedback', lazy='joined')

    def __repr__(self):
        return f'Feedback id: {self.id}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
