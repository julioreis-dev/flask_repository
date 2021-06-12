from threading import Thread
import requests
from apps.models import Criptocotation, User, CriptoTable, LogEmail
from apps import db, env
import smtplib
from time import localtime
from datetime import datetime
from dateutil.relativedelta import relativedelta


def add_price(tupla):
    """Função que registra na tabela Criptocotation a cotação oriunda do consumo da API."""
    newprice = Criptocotation(
        coin_name=tupla[0],
        price=tupla[1],
        variation=tupla[2],
        date=datetime.now()
    )
    db.session.add(newprice)
    db.session.commit()


def all_coins(coin):
    """Função que retorna o ultimo registro de uma determinada criptocoin."""
    data = db.session.query(Criptocotation).filter_by(coin_name=coin).all()
    if not data:
        return None
    else:
        return data[-1]


def call_api():
    """Função que consome a API que fornece as cotações atuais das criptocoins."""
    bit_price = 'https://api.coincap.io/v2/assets/{}'
    coins = {'BTC': 'Bitcoin', 'LINK': 'Chainlink', 'XRP': 'XRP', 'LTC': 'Litecoin', 'CHZ': 'Chiliz', 'ETH': 'Ethereum',
             'DOGE': 'Dogecoin', 'ADA': 'Cardano'}
    for coin in coins:
        adress = bit_price.format(coins[coin].lower())
        response = requests.get(adress)
        result = response.json()
        name_coin = result["data"]["name"]
        price_round = round(float(result["data"]["priceUsd"]), 2)
        var_round = round(float(result["data"]["changePercent24Hr"]), 2)
        tupla_result = (name_coin, price_round, var_round)
        add_price(tupla_result)


def greet():
    """Função que retorna o tratamento adequado de acordo com o horário."""
    t = localtime()
    if t[3] < 12:
        return 'Bom dia!!!'
    elif t[3] > 18:
        return 'Boa noite!!!'
    else:
        return 'Boa tarde!!!'


def preparation(user, coins):
    """Função que retorna a mensagem de email com base nos parametros cadastrados pelo cliente."""
    current_cotation = all_coins(coins.coin)
    if current_cotation.price > float(coins.sell):
        status = f'Prezado(a) {user.name}, {greet()}\nCom base nos parametros cadastrados na plataforma de ' \
                 f'monitoramento.\nEstamos emitindo o seguinte comunicado:' \
                 f'\n#####################################################################################' \
                 f'\n\nRelatorio:\nCriptocoin: {coins.coin}\npreco atual: ${current_cotation.price}\nAnalise preliminar: ' \
                 f'O Ativo encontra-se com o preco acima do valor cadastrado para a operacao de venda que e de ${coins.sell}.' \
                 f'\nRecomendacao: Recomendamos que o cliente realize a venda do referido ativo.' \
                 f'\n\n#####################################################################################'

    elif current_cotation.price <= float(coins.buy):
        status = f'Prezado(a) {user.name}, {greet()}\nCom base nos parametros cadastrados na plataforma de ' \
                 f'monitoramento.\nEstamos emitindo o seguinte comunicado:' \
                 f'\n#####################################################################################' \
                 f'\n\nRelatorio:\nCriptocoin: {coins.coin}\npreco atual: ${current_cotation.price}\nAnalise preliminar: ' \
                 f'O Ativo encontra-se com o preco abaixo do valor cadastrado para a operacao de compra que e de ${coins.buy}.' \
                 f'\nRecomendacao: Recomendamos que o cliente realize a compra do referido ativo.' \
                 f'\n\n#####################################################################################'
    else:
        status = None
    return status


def sent_mail(dest, msg, name):
    """
    Função que envia email
    """
    my_email = env.str('NT_EMAIL')
    my_password = env.str('NT_EMAIL_PASSWORD')
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(from_addr=my_email, to_addrs=dest,
                           msg=f'Subject:Cripto Cotacoes - Alerta de Monitoramento ({name})\n\n{msg}')


def monitor_data():
    """
    Função que monitora os parametros cadastrados por cada cliente
    """
    info_user = all_users()
    if info_user is not None:
        for informes in info_user:
            check = Thread(target=check_assets, args=[informes])
            check.start()


def check_assets(info):
    """
    Função que monitora e encaminha os emails de alerta de acordo com o timer estabelecido pelo cliente
    """
    info_coins = general_info(info.id)
    if info_coins is not None:
        for each in info_coins:
            quote = preparation(info, each)
            if quote is not None:
                logs = all_logs(info.id, each.id)
                if logs is None:
                    add_log(info, each)
                    first_mail = Thread(target=sent_mail, args=[info.email, quote, each.coin])
                    first_mail.start()
                else:
                    last = last_log(info.id, each.id)
                    dif = abs(relativedelta(datetime.now(), last.date))
                    record = record_user(info.id, each.coin)
                    if dif.hours != 0:
                        add_log(info, each)
                        mail = Thread(target=sent_mail, args=[info.email, quote, each.coin])
                        mail.start()
                    elif dif.minutes >= record.timer:
                        add_log(info, each)
                        mail = Thread(target=sent_mail, args=[info.email, quote, each.coin])
                        mail.start()



def add_log(user, current_coin):
    """
    Função que registra na tabela log_table todos emails de alerta encaminhados para os clientes
    """
    newlog = LogEmail(
        date=datetime.now(),
        user_id=user.id,
        coin_id=current_coin.id,
    )
    db.session.add(newlog)
    db.session.commit()


def all_logs(id_number, id_coin):
    """
    Função que retorna todas os emails de alerta encaminhado a um cliente referente a uma determinada criptocoin
    """
    data = db.session.query(LogEmail).filter(LogEmail.user_id == id_number).filter(LogEmail.coin_id == id_coin).all()
    if not data:
        return None
    else:
        return data


def last_log(id_number, id_coin):
    """
    Função que retorna o ultimo registro de email de alerta encaminhado a um cliente referente a uma
    determinada criptocoin
    """
    data = db.session.query(LogEmail).filter(LogEmail.user_id == id_number).filter(LogEmail.coin_id == id_coin).all()
    if not data:
        return None
    else:
        return data[-1]


def record_user(id_number, name_coin):
    """
    Função que retorna o primeiro registro de um cliente referente a uma determinada criptocoin
    """
    data = db.session.query(CriptoTable).filter(CriptoTable.user_id == id_number).filter(
        CriptoTable.coin == name_coin).first()
    if not data:
        return None
    else:
        return data


def all_users():
    """
    Função que retorna todos os usuários
    """
    data = db.session.query(User).all()
    if not data:
        return None
    else:
        return data


def general_info(user):
    """
    Função que retorna todos os registros referente aos critérios estabelecidos por uma determinado cliente
    """
    data = db.session.query(CriptoTable).filter_by(user_id=user).all()
    return data
