#-*- coding: utf-8 -*-
import time

def read_file_and_delete_line():
    time.sleep(1)
    read_f = open("target.txt", "r")
    check = read_f.read()
    save_data = str(check[:check.find('\n')+1])

    write_f = open("target.txt", "w")
    write_f.write(check.replace(check[:check.find('\n')+1], ''))
    write_f.close()
    read_f.close()

    if check == '':
        pass
    else:
        print(save_data)
        pass


while True:
    read_file_and_delete_line()
    time.sleep(5)


