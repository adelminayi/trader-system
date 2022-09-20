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


    apk =decrypt('a3e5/T08ZGdoxlpjdS0yKuv1C6Nvlii+fdAFop0SBTBH1hG/Zbc2TavVnSTFq6uaV+lA/+hdqT8Zu0XKdhNqpA==*6tWYuc0fQ7hDFoLz5Ui4KA==*V1vB1/JbTXM0KQnw3uIgOA==*7tSV08++KAt9a1Axkb2yzA==', APIKEYPASS)
    sctkey = decrypt('PgWqKQWjadKCUdzTPHUiWZzjApiNA9+BSvtD8Y0RMV1bNPSI9P3IsdUOXDEeITnRzSEH+Rz+TKwVLC3qvpMWmg==*V33WhUjnMEEJgxIGZ15jQA==*leqdy04uakRANVZgB2TLuA==*ml3322DJ7Z6gxIwLIDO7lg==', SECKEYPASS)
    print(apk)
    print(sctkey)


get_api_keys()