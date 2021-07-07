"""
    made by hyeonbell 2021.07.07
    # ref : https://lightning.bitflyer.com/docs?lang=ja#%E8%AA%8D%E8%A8%BC
    # var text = timestamp + method + path + body;
    # var sign = crypto.createHmac('sha256', secret).update(text).digest('hex');


    C:\code>python hmac_create.py
    64be2a34ff4acb031d46269f041b53ab611b67c4b1d3ddd83bf5bbb4949ad368

"""

import hmac
import time
import hashlib

# value setup
now = time.localtime()

secret = "Your_Secret_Key".encode()
timestamp = "{}/{}/{} {}:{}:{}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
method = "GET"
path = "/"

body = """
content
"""
plaintext = (str(timestamp) + method + path + body).encode()

# hmac setup

hash_module = hmac.new(secret, plaintext, hashlib.sha256)
digest_value = hash_module.hexdigest()

# Output
print(digest_value)
