# Made by hyeonbell
# 2018/01/21
import sys

filename = sys.argv[1]
f = open(filename)
data = f.read()
result = {}

hexdata = data.encode("hex")
s = ''
i = 0

while i < len(hexdata):
    cursor = hexdata[i:i+2]
    if not (cursor in result):
        result[cursor] = 1
    else:
        result[cursor] = result[cursor] + 1
    i = i + 2
inverse = [(value, key) for key, value in result.items()]
maxv = max(inverse)
print("-"*28+"\n\t[RESULT]\n"+"-"*28+"\n")
print("Max frequency hex is " + str(maxv[1]) + " = " + str(maxv[0]))
print("Character is " + maxv[1].decode("hex"))
print("\n"+"-"*28)
