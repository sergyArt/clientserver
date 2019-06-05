from socket import *
import time

s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
s.bind(('', 7777))                # Присваивает порт 8888
s.listen(5)                       # Переходит в режим ожидания запросов;
                                  # одновременно обслуживает не более
                                  # 5 запросов.
while True:
    client, addr = s.accept()     # Принять запрос на соединение
    print("Получен запрос на соединение от %s" % str(addr))
    timestr = time.ctime(time.time()) + "\n"
    client.send(timestr.encode('ascii'))
    client.close()
