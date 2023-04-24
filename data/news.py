import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("citizens.id"))
    user = orm.relationship('User')


class NewsForm(FlaskForm):
    content = TextAreaField("Содержание", validators=[DataRequired()])
    submit = SubmitField('Применить')