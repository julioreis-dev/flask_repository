from . import home
from flask import render_template
from apps.home.crud import all_coins, call_api


@home.route('/')
def index():
    """
    Função de abertura da página principal
    """
    list_result = []
    coins = {'BTC': 'Bitcoin', 'LINK': 'Chainlink', 'XRP': 'XRP', 'LTC': 'Litecoin', 'CHZ': 'Chiliz', 'ETH': 'Ethereum',
             'DOGE': 'Dogecoin', 'ADA': 'Cardano'}
    for coin in coins:
        if all_coins(coins[coin]) is None:
            call_api()
            list_result.append(all_coins(coins[coin]))
        else:
            list_result.append(all_coins(coins[coin]))
    return render_template('index.html', all_results=list_result)
