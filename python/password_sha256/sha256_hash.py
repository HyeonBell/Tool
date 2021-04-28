import hashlib
import random

ran=""
for i in range(0,5):
   ran += str(random.randint(1,10))
   print(ran)

string = "secret_password"+ran
encode_s = string.encode()
print(encode_s)
hexdigest = hashlib.sha256(encode_s).hexdigest()
print('password digest : ', hexdigest)
