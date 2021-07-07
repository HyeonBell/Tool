"""
    made by hyeonbell 21.07.05
    simple api request for test or expanding functionality in complex program
    ref : postman tool

"""


import requests
import base64

url = "https://target.test.com/api2/cvi/"

payload = "payload base64 or string or ............."
headers = {
  'Content-Type': 'application/json',
  'Cookie': '0ea0a1d2062c664b99378c2c04775b2e53c67572=7304lmk8nuc7gr331rc98fcj0'
}

temp = eval(base64.b64decode(payload))
temp['user'] = 'id" password="1111" --'
temp['password'] = '1234'

# dict type stirng replace
temp = str(temp).replace("","").replace("{\'","{\"")
temp = temp.replace("\':", "\":")
temp = temp.replace(": \'", ": \"")
temp = temp.replace("\',", "\",")
temp = temp.replace(", \'", ", \"")
temp = temp.replace("\'}", "\"}")
temp = temp.replace("\\", "")
payload = base64.b64encode(temp.encode()).decode()


print("final : " + str(payload))
print(base64.b64decode(payload))

response = requests.request("POST", url, headers=headers, data=payload)

# output
print(response.text)
