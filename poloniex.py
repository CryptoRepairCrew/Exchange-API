import urllib
import urllib2
import json
import time
import hmac,hashlib
import requests

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

class poloniex:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def post_process(self, before):
        after = before

        # Add timestamps if there isnt one but is a datetime
        if('return' in after):
            if(isinstance(after['return'], list)):
                for x in xrange(0, len(after['return'])):
                    if(isinstance(after['return'][x], dict)):
                        if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))
                            
        return after

    def api_query(self, uri,  type='GET', payload={}):
	if type == 'GET':
	   r = requests.get(uri, params=payload)
	   return r
	else:
            payload['nonce'] = int(time.time()*1000)
            post_data = urllib.urlencode(payload)
            sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()
            headers = {
                'Sign': sign,
                'Key': self.APIKey
            }
	    r = requests.post(uri, data=payload, headers=headers)
	    
	    return r

    # Public API Methods
    # Return the Ticker for ALL Markets 
    def returnTicker(self):
        return self.api_query("https://poloniex.com/public?command=returnTicker")

    # Returns the 24 H Volume for all Markets + Totals For Primary Currencies
    def return24Volume(self):
        return self.api_query("https://poloniex.com/public?command=return24hVolume")

    # Returns the Order Book For a Market
    def returnOrderBook (self, currencyPair):
	payload = {'currencyPair': currencyPair }
        return self.api_query("https://poloniex.com/public?command=returnOrderBook", payload=payload)

    # Returns the Past 200 Trades for a Given Market
    def returnMarketTradeHistory (self, currencyPair):
	payload = {'currencyPair': currencyPair}
        return self.api_query("https://poloniex.com/public?command=returnTradeHistory", payload=payload)

    # Trading API Methods
    # Returns all of your balances.
    def returnBalances(self):
	payload = {'command': 'returnBalances' }
        return self.api_query("https://poloniex.com/tradingApi", payload=payload, type='POST')

    # Returns all of your deposit addresses.
    def returnDepositAddreses(self):
	payload = {'command': 'returnDepositAddresses'}
	return self.api_query("https://poloniex.com/tradingApi", payload=payload, type='POST')
 
    # Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP"
    def returnOpenOrders(self,currencyPair):
	payload = {'command': 'returnOpenOrders','currencyPair': currencyPair }
        return self.api_query('https://poloniex.com/tradingApi', payload=payload, type='POST')

    # Returns your trade history for a given market, specified by the "currencyPair" POST parameter
    def returnTradeHistory(self,currencyPair):
	payload = {'command': 'returnTradeHistory', 'currencyPair': currencyPair }
        return self.api_query('https://poloniex.com/tradingApi', payload=payload, type='POST')

    # Places a buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    def buy(self,currencyPair,rate,amount):
	payload = {'command': 'buy', 'currencyPair':currencyPair,'rate':rate,'amount':amount}
        return self.api_query('https://poloniex.com/tradingApi', payload=payload, type='POST')

    # Places a sell order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    def sell(self,currencyPair,rate,amount):
	payload = {'command': 'sell', 'currencyPair':currencyPair,'rate':rate,'amount':amount}
        return self.api_query('https://poloniex.com/tradingApi', payload=payload, type='POST')

    # Cancels an order you have placed in a given market. Required POST parameters are "currencyPair" and "orderNumber".
    def cancel(self,currencyPair,orderNumber):
	payload = {'command': 'cancelOrder', 'currencyPair':currencyPair,'orderNumber':orderNumber}
        return self.api_query('https://poloniex.com/tradingApi', payload=payload, type='POST')

    # Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method, the withdrawal privilege must be enabled for your API key. Required POST parameters are "currency", "amount", and "address". Sample output: {"response":"Withdrew 2398 NXT."} 
    def withdraw(self, currency, amount, address):
	paylod = {'command': 'withdraw', 'currency':currency, 'amount':amount, 'address':address }
        return self.api_query('https://poloniex.com/tradingApi', payload=payload, type='POST')
