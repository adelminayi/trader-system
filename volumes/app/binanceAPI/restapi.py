import hmac
from pydoc import cli
import time
import hashlib
import requests
from urllib.parse import urlencode

from pprint import pprint


# from binance.client import Client

class Binance:
    def __init__(self,
                apiKey      :   str = "",
                secretKey   :   str = ""):

        self.apiKey     = apiKey
        self.secretKey  = secretKey
        self.SPOT_URL   = "https://api.binance.com"
        self.FUTURES_URL= "https://fapi.binance.com"
        
    def hashing(self,secretKey,query_string):
        return hmac.new(secretKey.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def get_timestamp(self,):
        return int(time.time() * 1000)

    def dispatch_request(self,key,http_method):
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'X-MBX-APIKEY': key
        })
        return {
            'GET': session.get,
            'DELETE': session.delete,
            'PUT': session.put,
            'POST': session.post,
        }.get(http_method, 'GET')

    def apiKeyPermission(self):
        query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.SPOT_URL + '/sapi/v1/account/apiRestrictions?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        # print('url:', url,'\n')
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        # print('apiKeyPermission response: ', response.status_code)
        return response.json()

    def accountStatus(self,):
        query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.SPOT_URL + '/sapi/v1/account/status?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def accountAPIStatus(self,):
        query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.SPOT_URL + '/sapi/v1/account/apiTradingStatus?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def depositHistory(self, coin):
        query_string = urlencode({
                                'coin':coin
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.SPOT_URL + '/sapi/v1/capital/deposit/hisrec?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def withdrawHistory(self, coin):
        query_string = urlencode({
                                'coin':coin
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.SPOT_URL + '/sapi/v1/capital/withdraw/history?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def spotCoins(self,):
        query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.SPOT_URL + '/sapi/v1/capital/config/getall?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def futuresBalance(self,):
        query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v2/balance?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        print(url)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def futuresTrades(self, symbol, startTime, endTime, limit):
        query_string = urlencode({
                                'symbol':symbol, 
                                'startTime':startTime, 
                                'endTime':endTime, 
                                'limit':limit
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/userTrades?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def lastTrades(self, symbol, limit):
        query_string = urlencode({
                                'symbol':symbol, 
                                'limit':limit
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/userTrades?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()
        
    def lastOrders(self, symbol, startTime, endTime, limit): 
        query_string = urlencode({
                                'symbol':symbol,
                                'startTime':startTime,
                                'endTime':endTime,
                                'limit':limit
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/allOrders?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()
    
    def currentOrders(self, symbol):
        query_string = urlencode({
                                'symbol':symbol
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/openOrders?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def cancelAllOrders(self, symbol): 
        query_string = urlencode({
                                'symbol':symbol
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/allOpenOrders?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'DELETE')(url=url)
        return response.json()

    def cancelOrder(self, orderId, symbol): 
        query_string = urlencode({
                                'symbol':symbol, 
                                'orderId':orderId
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/order?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'DELETE')(url=url)
        return response.json()

    def clientOrderId(self,):
        return str(int(time.time() * 1000))

    def marketOrder(self, symbol, side, quantity): 
        clientOrderId = self.clientOrderId()
        query_string = urlencode({
                                'symbol':symbol, 
                                'side':side, 
                                'type':'MARKET', 
                                'quantity':quantity,
                                'newClientOrderId': clientOrderId
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/order?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey, 'POST')(url=url)
        return response.json()

    def limitOrder(self, symbol, side, quantity, price): 
        query_string = urlencode({
                                'symbol':symbol, 
                                'side':side, 
                                'type':'LIMIT',
                                'timeInForce':'GTC', 
                                'quantity':quantity,
                                'price':price,
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/order?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'POST')(url=url)
        return response.json()

    def stopOrder(self, symbol, side, quantity, price, stopPrice, workingType, priceProtect): 
        query_string = urlencode({
                                'symbol':symbol, 
                                'side':side, 
                                'type':'STOP',
                                'timeInForce':'GTC', 
                                'quantity':quantity,
                                'price':price,
                                'stopPrice':stopPrice,
                                'workingType':workingType,
                                'priceProtect':priceProtect
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/order?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'POST')(url=url)
        return response.json()

    def takeProfitOrder(self, symbol, side, quantity, price, stopPrice, workingType, priceProtect): 
        query_string = urlencode({
                                'symbol': symbol, 
                                'side':side, 
                                'type':'TAKE_PROFIT',
                                'timeInForce':'GTC', 
                                'quantity':quantity,
                                'price':price,
                                'stopPrice':stopPrice,
                                'workingType':workingType,
                                'priceProtect':priceProtect
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/order?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'POST')(url=url)
        return response.json()

    def trailStopOrder(self, symbol, side, quantity, activationPrice, callbackRate, workingType): 
        query_string = urlencode({
                                'symbol':symbol, 
                                'side':side, 
                                'type':'TRAILING_STOP_MARKET',
                                'timeInForce':'GTC', 
                                'quantity':quantity,
                                'activationPrice':activationPrice,
                                'callbackRate':callbackRate,
                                'workingType':workingType
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/order?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'POST')(url=url)
        return response.json()

    def currentPositions(self, symbol): 
        query_string = urlencode({
                                'symbol':symbol
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v2/positionRisk?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def closeCurrentPositions(self, symbol):
        query_string = urlencode({
                            'symbol':symbol
                            })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v2/positionRisk?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        res      = response.json()[0]
        side     = float(res['positionAmt'])
        positionAmt = str(abs(float(res['positionAmt'])))
        if float(positionAmt) != 0.0:
            if side>0:
                query_string = urlencode({
                                'symbol':symbol, 
                                'side':'SELL', 
                                'type':'MARKET', 
                                'quantity':positionAmt
                                })
                query_string = query_string.replace('%27', '%22')                                           
                if query_string:
                    query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
                else:
                    query_string = 'timestamp={}'.format(self.get_timestamp())
                url = self.FUTURES_URL + '/fapi/v1/order?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
                response = self.dispatch_request(self.apiKey,'POST')(url=url)
                response = response.json()
            elif side<0:
                query_string = urlencode({
                                'symbol':symbol, 
                                'side':'BUY', 
                                'type':'MARKET', 
                                'quantity':positionAmt
                                })
                query_string = query_string.replace('%27', '%22')                                           
                if query_string:
                    query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
                else:
                    query_string = 'timestamp={}'.format(self.get_timestamp())
                url = self.FUTURES_URL + '/fapi/v1/order?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
                response = self.dispatch_request(self.apiKey,'POST')(url=url)
                response = response.json()
            return response
        return "No position was taken."

    def changeMarginType(self, symbol, marginType): 
        query_string = urlencode({
                                'symbol':symbol, 
                                'marginType':marginType
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/marginType?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'POST')(url=url)
        return response.json()

    def changeLeverage(self, symbol, leverage): 
        query_string = urlencode({
                                'symbol':symbol, 
                                'leverage':leverage
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/leverage?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'POST')(url=url)
        return response.json()

    def isDualSidePosition(self):                                          
        query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/positionSide/dual?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()

    def dualSidePosition(self,dualSidePosition): 
        query_string = urlencode({
                                'dualSidePosition':dualSidePosition
                                })
        query_string = query_string.replace('%27', '%22')                                           
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v1/positionSide/dual?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'POST')(url=url)
        return response.json()

    def accountInfo(self):                                          
        query_string = 'timestamp={}'.format(self.get_timestamp())
        url = self.FUTURES_URL + '/fapi/v2/account?' + query_string + '&signature=' + self.hashing(self.secretKey,query_string)
        response = self.dispatch_request(self.apiKey,'GET')(url=url)
        return response.json()
    
    # def deposit_address_supporting_network(self):
    #     query_string = 'timestamp={}'.format(self.get_timestamp())
    #     print(adel := self.hashing(self.secretKey,query_string))
    #     url = 'https://api.binance.com/sapi/v1/capital/config/getall?&{}&signature={}}'.format(query_string, adel)
    #     response = self.dispatch_request(self.apiKey,'GET')(url=url)
    #     return response.json()


if __name__=="__main__":
    import time
    apiKey    = "aWJZ533J0ty18hBdUHHBKp5AOKvq2jXeWyP3m8WrWbyGJ8jBq9cvix1TlJQTxRtt"
    secretKey = "QhNUo82PM9CnZxLVDP27bcODdYPZY0sUQPCHgcQS0nq4qo06r3gcVSYnd00FvBwn"
    bin = Binance(apiKey, secretKey)
    # res = bin.apiKeyPermission()
    # print(res)
    # pprint(bin.futuresBalance()[6]['balance'])
    # pprint(res)



