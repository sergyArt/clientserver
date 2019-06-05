from socket import *

s = socket(AF_INET,SOCK_STREAM)  # Создать сокет TCP
s.connect(('localhost', 7777))   # Соединиться с сервером
tm = s.recv(1024)                # Принять не более 1024 байтов данных
s.close()
print("Текущее время: %s" % tm.decode('ascii'))
