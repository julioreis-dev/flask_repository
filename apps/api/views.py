from . import api
from flask import jsonify, request
from apps import db
from apps.models import Criptocotation
from datetime import datetime


# _____________________________ HTTP GET - Read Record ____________________________________ #
@api.route("/api/<coin_name>", methods=['GET', 'POST'])
def coin_content(coin_name):
    """Função que retorna um JSON com todos os registros de uma determinada criptocoin."""
    if coin_name.lower() == 'xrp':
        name = coin_name.upper()
    else:
        name = coin_name.capitalize()
    coin = db.session.query(Criptocotation).filter_by(coin_name=name).all()
    return jsonify(info=[cotation.to_dict() for cotation in coin])


@api.route("/api/all", methods=['GET', 'POST'])
def all_content():
    """Função que retorna um JSON com todos os registros de todas as criptocoins."""
    all_coins = db.session.query(Criptocotation).all()
    return jsonify(all=[cotation.to_dict() for cotation in all_coins])


@api.route("/api/data", methods=['GET', 'POST'])
def period_content():
    """Função que retorna um JSON com todos os registros a partir de uma data até o momento atual."""
    datas = request.args.get('day')
    correct_data = datetime.strptime(datas, '%d-%m-%Y')
    period = db.session.query(Criptocotation).filter(Criptocotation.date >= correct_data).all()
    return jsonify(period=[cotation.to_dict() for cotation in period])


@api.route("/api/period", methods=['GET', 'POST'])
def periodcripto_content():
    """Função que retorna um JSON com todos os registros de uma determinada criptocoin a partir de uma data até o
    momento atual. """
    datas = request.args.get('day')
    coin = request.args.get('name')
    if coin.lower() == 'xrp':
        name = coin.upper()
    else:
        name = coin.capitalize()
    correct_data = datetime.strptime(datas, '%d-%m-%Y')
    info = db.session.query(Criptocotation).filter(Criptocotation.date >= correct_data).filter(
        Criptocotation.coin_name == name).all()
    return jsonify(period=[cotation.to_dict() for cotation in info])
