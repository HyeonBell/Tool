#-*- encoding:utf-8 -*-
import re
import sys

print(sys.argv[1])
f = open(sys.argv[1],'rt', encoding='cp949')
data = f.read()
print(data)
replace_d = re.sub(',', '\n',data)

f_replace = open(sys.argv[1][:-4]+'_replace.txt', 'wt', encoding='cp949')
f_replace.write(replace_d)

f.close()
f_replace.close()