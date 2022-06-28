import os
import json
# import hashlib
import requests
from dotenv import load_dotenv
# from datetime import datetime
from random import randrange

from kavenegar import *

from redis import Redis



load_dotenv()
REDIS_HOST     = os.getenv('REDIS_HOST')
REDIS_PORT     = os.getenv('REDIS_PORT')
REDIS_DB       = os.getenv('REDIS_DB')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


r = Redis(
        host    = REDIS_HOST, 
        port    = int(REDIS_PORT), 
        db      = int(REDIS_DB),
        password= REDIS_PASSWORD
    )

class APIException(Exception):
    pass

class HTTPException(Exception):
    pass


"""Default requests timeout in seconds."""
DEFAULT_TIMEOUT = 10
EXPIRATION_TIME = 10*60

class KavenegarAPI(object):
    def __init__(self, apikey, timeout=None, exptime=None):
        self.version = 'v1'
        self.host = 'api.kavenegar.com'
        self.apikey = apikey
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.exptime = exptime or EXPIRATION_TIME
        self.headers = {
	    'Accept': 'application/json',
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'charset': 'utf-8'
            }
        
    def __repr__(self):
        return "kavenegar.KavenegarAPI({!r})".format(self.apikey)

    def __str__(self):
        return "kavenegar.KavenegarAPI({!s})".format(self.apikey)

    def code_generator(self, phone_number):
        # return hashlib.md5((phone_number+str(datetime.now())).encode()).hexdigest()[:6]
        return str(randrange(100000, 999999))

    def _request(self, action, method, params={}):
        url = 'https://'+self.host+'/'+self.version+'/'+self.apikey+'/'+action+'/'+method+'.json'
        try:
            content = requests.post(url,headers=self.headers,auth=None,data=params,timeout=self.timeout).content
            try:
                response = json.loads(content.decode("utf-8"))
                if (response['return']['status']==200):
                    response=response['entries']
                else:
                    raise APIException('APIException[{}] {}'.format(response['return']['status'],response['return']['message']))
            except ValueError as e:
                raise HTTPException(e)
            return (response)
        except requests.exceptions.RequestException as e:
            raise HTTPException(e)
        
    def sms_send(self, phone_number):
        code    = self.code_generator(phone_number)
        #params  = "receptor={}&sender=0018018949161&message=Your Actication Code: {}".format(phone_number,code)
        params = {
        'receptor': phone_number, # your number
        'template': 'VerifyJirnal',
        'token': code, # your code
        }
        r.lpush(code, phone_number)
        r.expire(code, self.exptime)
        return self._request('verify', 'lookup',params)
    
    def sms_sendarray(self, params=None):
        return self._request('sms', 'sendarray',params)
    
    def sms_status(self, params=None):
        return self._request('sms', 'status',params)
    
    def sms_statuslocalmessageid(self, params=None):
        return self._request('sms', 'statuslocalmessageid',params)
    
    def sms_select(self, params=None):
        return self._request('sms', 'select',params)
    
    def sms_selectoutbox(self, params=None):
        return self._request('sms', 'selectoutbox',params)
    
    def sms_latestoutbox(self, params=None):
        return self._request('sms', 'latestoutbox',params)
    
    def sms_countoutbox(self, params=None):
        return self._request('sms', 'countoutbox',params)
    
    def sms_cancel(self, params=None):
        return self._request('sms', 'cancel',params)
    
    def sms_receive(self, params=None):
        return self._request('sms', 'receive',params)
    
    def sms_countinbox(self, params=None):
        return self._request('sms', 'countinbox',params)
    
    def sms_countpostalcode(self, params=None):
        return self._request('sms', 'countpostalcode',params)
    
    def sms_sendbypostalcode(self, params=None):
        return self._request('sms', 'sendbypostalcode',params)
    
    def verify_lookup(self, params=None):
        return self._request('verify', 'lookup',params)
    
    def call_maketts(self, params=None):
        return self._request('call', 'maketts',params)   
		
    def call_status(self, params=None):
        return self._request('call', 'status',params)   
    
    def account_info(self):
        return self._request('account', 'info')
    
    def account_config(self ,params=None):
        return self._request('account', 'config',params)   




# if __name__ == "__main__":
#     ins = KavenegarAPI(apikey="56476D374E69424F6D4F4B61682F44506D356A3453513D3D")
#     ins.sms_send("09910462926")
