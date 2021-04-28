import re

password = "!Wemdl1589"

safe_length = 10

#  특수 문자
sp_regex = re.compile('[!@#\$%\^&*\(\)]')
m = sp_regex.match(password)
if m:
    print(m.group())
    print("특수문자 통과")

# 길이
if len(password) >= safe_length:
    print(len(password))
    print("길이 통과")

# 소문자
lower_regex = re.compile('[a-z]')
m = lower_regex.findall(password)
if m:
    print(m)
    print("소문자 통과")

# 대문자
upper_regex = re.compile('[A-Z]')
m = upper_regex.findall(password)
if m:
    print(m)
    print("대문자 통과")

# 숫자
digit_regex = re.compile('[0-9]')
m = digit_regex.findall(password)
if m:
    print(m)
    print("숫자 통과")

