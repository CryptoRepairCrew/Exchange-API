import json
import time
import hmac,hashlib
import requests
import urllib
 
# Bittrex API Class 
class bittrex:

   # Init the Class With the Bittrex API Key and API Secret
   def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

   # Use This to query the API. 
   # NOTE: For Use Internally Only
   def api_query(self, uri, type='GET', payload={}):
	sign = hmac.new(self.Secret, uri + '?' + urllib.urlencode(payload), hashlib.sha512).hexdigest()
	headers = {'apisign': sign }
	if type == 'GET':
	   r = requests.get(uri, params=payload, headers=headers)
	else:
	   r = requests.post(uri, params=payload, headers=headers)
        return r

   # Public Requests
   # Get All Market's 
   def getMarkets(self):
	return self.api_query("https://bittrex.com/api/v1.1/public/getmarkets")

   # Get All Currencies
   def getCurrencies(self):
	return self.api_query("https://bittrex.com/api/v1.1/public/getcurrencies")

   # Get Ticker For 1 Market
   def getTicker(self, market):
	return self.api_query("https://bittrex.com/api/v1.1/public/getticker", payload={'market': market})

   # Get 24 Hour Stats Summary For all Active Markets
   def getMarketSummaries(self):
	return self.api_query("https://bittrex.com/api/v1.1/public/getmarketsummaries")

   # Get OrderBook
   def getOrderBook(self, market, type, depth=20):
	return self.api_query("https://bittrex.com/api/v1.1/public/getorderbook", payload={'market':market, 'type':type, 'depth':depth})

   # Market Requests
   # Get Market History
   def getMarketHistory(self, market, count=20):
       return self.api_query("https://bittrex.com/v1.1/public/getmarkethistory", payload={'market':market, 'count':count})

   # Place a LIMIT BUY Order
   def placeBuyOrder(self, market, quantity, rate):
       params = {'apikey': self.APIKey, 'market':market, 'quantity': quantity, 'rate': rate}
       return self.api_query("https://bittrex.com/v1.1/market/buylimit", payload = params)

   # Place a LIMIT SELL Order
   def placeSellOrder(self, market, quantity, rate):
       params = {'apikey': self.APIKey, 'market':market, 'quantity': quantity, 'rate': rate}
       return self.api_query("https://bittrex.com/v1.1/market/selllimit", payload = params)

   # Cancel an Order
   def cancelOrder(self, uuid):
       params = {'apikey': self.APIKey, 'uuid': uuid}
       return self.api_query("https://bittrex.com/v1.1/market/cancel", payload = params)

   # Get All Open Orders
   def getOpenOrders(self, market):
       params = {'apikey': self.APIKey, 'market':market}
       return self.api_query("https://bittrex.com/v1.1/market/getopenorders", payload=params)


   # Account Requests
   # Get All Blances
   def getBalances(self):
       params = {'apikey': self.APIKey, 'nonce': int(time.time())}
       return self.api_query("https://bittrex.com/api/v1.1/account/getbalances", payload=params)

   # Get 1 Coins Balance
   def getBalance(self, currency):
       params = {'apikey': self.APIKey, 'currency': currency}
       return self.api_query("https://bittrex.com/api/v1.1/account/getbalance", payload=params)

   # Get Deposit Address
   def getDepositAddress(self, currency):
       params = {'apikey': self.APIKey, 'currency': currency}
       return self.api_query("https://bittrex.com/api/v1.1/account/getdepositaddress", payload=params)

   # Withdraw Coins
   def withdrawCoins(self, currency, quantity, address):
       params = {'apikey': self.APIKey, 'currency': currency, 'quantity': quantity, 'address': address }
       return self.api_query("https://bittrex.com/api/v1.1/account/withdraw", payload=params)

   # Get Order History
   def getOrderHistory(self, market, count):
       params = {'apikey': self.APIKey, 'count': count}
       return self.api_query("https://bittrex.com/api/v1.1/account/getorderhistory", payload=params)

   # Get Withdrawal History
   def getWithdrawalHistory(self, currency, count):
       params = {'apikey': self.APIKey, 'currency': currency, 'count': count}
       return self.api_query("https://bittrex.com/api/v1.1/account/getwithdrawalhistory", payload=params)

   # Get Deposit History
   def getDepositHistory(self, currency, count):
       params = {'apikey': self.APIKey, 'currency': currency, 'count': count }
       return self.api_query("https://bittrex.com/v1.1/account/getdeposithistory", payload=params)
