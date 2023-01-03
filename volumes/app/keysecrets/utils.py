import os
from telnetlib import ENCRYPT
from cryptocode import decrypt, encrypt
from dotenv import load_dotenv




load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')

def get_api_keys():
    # binance = Binance(
    #                         decrypt(apiKey, APIKEYPASS), 
    #                         decrypt(secretKey, SECKEYPASS)
    #                 )
    # apk = encrypt('aWJZ533J0ty18hBdUHHBKp5AOKvq2jXeWyP3m8WrWbyGJ8jBq9cvix1TlJQTxRtA', APIKEYPASS)
    # sctkey =encrypt('QhNUo82PM9CnZxLVDP27bcODdYPZY0sUQPCHgcQS0nq4qo06r3gcVSYnd00FvBwn', SECKEYPASS)


    apk =decrypt('AEKbA/6U7JSw8N8z7ucmCtKwFSXrdeCG9W68Veit0gxgJELa5JecVUDlUOHgEfWupS30Jqdsu3VnsckA+zkngg==*cKdKbdcUZoR77HoRAlWGAQ==*4EKNfjJZ0N/ToTD5WHf4zg==*ybdcXH5ermZ3MrRUTvaflA==', APIKEYPASS)
    sctkey = decrypt('QI6gODcVhq1bE0pA1fxz8TCkzSxw0e+z0SlxpkjRlY2KkQTD8kUX8AHbrNjtulirESK7ggk0MmfNRPkZsoHeag==*Ph4xuanazHHlOh6tIsyjAw==*MUL2izPq+rRiad8AeU+oQQ==*+t4go80ZGZf0UD9YijeDNA==', SECKEYPASS)
    print(apk)
    print(sctkey)


get_api_keys()