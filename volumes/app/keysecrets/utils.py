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


    apk =decrypt('e44FgPLQAaKIFmtkJl2z7JFgWsZiEMReXKmIUGfTg/3nJeCXmYFoiD1sJ6Vjw3CqSXKAsj5vrRIak6EBert6dA==*X8KcBptuKf8BoNtw2rEslw==*A5iv2CKqB9wlHp0PJm0Afg==*CuZpKff1cQI1LkIKGdU51w==', APIKEYPASS)
    sctkey = decrypt('zyc0I8HExFjWHu87mn2u57zGibNsLHsISACmpaz3L0AJrrlBp74r9R3b4v5gpYE6JP41Ljf8U5Z4X7hSqNXk+g==*npvRuJniy4jrfwTgG77EgA==*CwynALeptwzXnTC9p8yvJg==*FY9xykgoWHwqJR2ZV0MNgQ==', SECKEYPASS)
    print(apk)
    print(sctkey)


get_api_keys()