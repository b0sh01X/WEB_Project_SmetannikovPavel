import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Recept(SqlAlchemyBase):
    __tablename__ = 'recept'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    reg = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    autor = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    catalog_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("catalog.id"))
    user = orm.relationship('User')
    catalog = orm.relationship('Catalog')