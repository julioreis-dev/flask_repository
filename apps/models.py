from flask_login import UserMixin
from sqlalchemy.orm import relationship
from . import db


class User(UserMixin, db.Model):
    """Classe que cria a tabela users para cadastro dos usuários."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    rt_user = relationship('CriptoTable', back_populates="rt_coin")
    rt_logemail = relationship('LogEmail', back_populates="rt_cripto")


class CriptoTable(db.Model):
    """Classe que cria a tabela cripto_table para cadastro dos critérios de cada usuário."""
    __tablename__ = "cripto_table"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    coin = db.Column(db.String(250), nullable=False)
    sell = db.Column(db.String(250), nullable=False)
    buy = db.Column(db.String(250), nullable=False)
    timer = db.Column(db.Integer, nullable=False)
    rt_coin = relationship('User', back_populates="rt_user")
    rt = relationship('LogEmail', back_populates="tr")


class LogEmail(db.Model):
    """Classe que cria a tabela log_table para registro dos emails de alerta encaminhados para os diversos usuários."""
    __tablename__ = "log_table"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    coin_id = db.Column(db.Integer, db.ForeignKey("cripto_table.id"))
    date = db.Column(db.DATETIME)
    rt_cripto = relationship('User', back_populates="rt_logemail")
    tr = relationship('CriptoTable', back_populates="rt")


class Criptocotation(db.Model):
    """Classe que cria a tabela cripto_cotation para registro dos dados consumidos da API que informa a cotação atual
    de cada criptocoin. """
    __tablename__ = "cripto_cotation"
    id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float)
    variation = db.Column(db.Float)
    date = db.Column(db.DATETIME)

    def to_dict(self):
        """Método que retorna um dicionário relativo a cada registro da tabela cripto_cotation."""
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


db.create_all()
