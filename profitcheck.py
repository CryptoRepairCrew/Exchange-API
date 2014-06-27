from poloniex import poloniex
from bittrex import bittrex
from mintpal import mintpal
from collections import OrderedDict

# Init Our Exchange Manager Class
class ExchangeManager:
    def __init__(self):
	self.Poloniex = poloniex("","")
	self.Bittrex = bittrex("", "")
	self.Mintpal = mintpal("", "")

    # Market Related Queries
    # Begin Our Needed Queries
    def returnPrice(self, coin_code):
	prices = {}
	full_code = 'BTC_' + coin_code.upper()
	hyphenated_code = 'BTC-' + coin_code.upper()
	slashed_code = coin_code.upper() + '/BTC'
	prices['poloniex'] = float(self.Poloniex.returnTicker().json()[full_code]['last'])
	prices['bittrex']  = float(self.Bittrex.getTicker(hyphenated_code).json()['result']['Last'])
	prices['mintpal']  = float(self.Mintpal.getMarket(slashed_code).json()['data']['last_price'])
	return prices


