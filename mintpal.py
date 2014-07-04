import simplejson as json
import time
import hmac,hashlib
import requests
import urllib
 
# MintPal API Class 
class mintpal:

   # Init the Class With the Bittrex API Key and API Secret
   def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

   # Use This to query the API. 
   # NOTE: For Use Internally Only
   def api_query(self, command, type='GET', payload={}):
	# Get Mintpal's Timestamp
	r = requests.get("https://api.mintpal.com/timestamp")
	mint_time = json.loads(r.content)['data']
	apiUrl = "https://api.mintpal.com/v2/"
	if type == 'GET':
	   uri = str(apiUrl) + str(command) + "?time=" + str(mint_time) + "&key=" + str(self.APIKey)
	   if payload:
	     uri =  uri + "&" + urllib.urlencode(payload)
	   hash = hmac.new(self.Secret, uri, hashlib.sha256).hexdigest()
	   uri += "&hash=" + hash
	   r = requests.get(uri)
        return r

   # Market Summary
   def getMarket(self, coin):
       uri = "market/stats/" + coin
       return self.api_query(uri)

   # Account Requests
   # Get All Blances
   def getBalances(self):
       return self.getBalance("")

   # Get 1 Coins Balance
   def getBalance(self, currency):
       return self.api_query("wallet/balances/" + currency)

   # Get Deposit Address
   def getDepositAddress(self, currency):
       return self.api_query("wallet/depositaddress/" + currency)

   # Withdraw Coins
   def withdrawCoins(self, currency, quantity, address):
       params = {'address': address, 'ammount': quantity }
       return self.api_query("wallet/withdraw/" + currency, payload=params)

   # Get Order History
   def getOrderHistory(self, market, count):
       #order history not available on Mintpal
       return None

   # Get Withdrawal History
   def getWithdrawalHistory(self, currency, count):
       return self.api_query("wallet/withdrawals/" + currency + "/0/" + str(count))

   # Get Deposit History
   def getDepositHistory(self, currency, count):
       return self.api_query("wallet/deposits/" + currency + "/0/" + str(count))

