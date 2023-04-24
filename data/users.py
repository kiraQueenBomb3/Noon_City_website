import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'citizens'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, nullable=True) #, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sex = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    reputation = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    gun = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    news = orm.relationship("News", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
