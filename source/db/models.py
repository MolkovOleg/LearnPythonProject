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


class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    address = Column(String)
    city = Column(String)
    area = Column(String)
    owner_name = Column(String)
    rooms = Column(Integer)
    photos = Column(String)
    website = Column(String)
    feedbacks = relationship('Feedback', lazy='joined')

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
        return f'Feedback id: {self.id}, raiting: {self.raiting}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
