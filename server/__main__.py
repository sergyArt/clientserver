import yaml
import socket
import json
import logging
import select
from actions import resolve
from protocol import validate_request, make_response
from argparse import ArgumentParser
import threading


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server_log.log'),
        logging.StreamHandler()

    ]
)


parser = ArgumentParser(usage='python %(prog)s [options]')
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration file'
)
parser.add_argument(
    '-p', '--port', type=int,
    default=7777,
    help='TCP port to work server. Default: 7777'
)
parser.add_argument(
    '-a', '--ip_address', type=str,
    default='127.0.0.1',
    help='Network interface to work server (IP address). Default: 127.0.0.1'
)

args = parser.parse_args()

host = args.ip_address
port = args.port
buffersize = 4096
encoding = 'utf-8'

if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host')
        port = config.get('port')


requests =[]
connections = []


def read(client, requests, buffersize):
    b_request = client.recv(buffersize)
    requests.append(b_request)

def write(client, response):
    client.send(response)



try:
    sock = socket.socket()

    sock.bind((host, port))
    sock.setblocking(False)
    sock.listen(5)

    print(f'Server was started with {host}:{port}')

    while True:
        try:

            client, address = sock.accept()
            logging.info(f'client with address {address} was detected.')
            connections.append(client)
        except:
            pass

        rlist, wlist, xlist = select.select(connections, connections, connections, 0)

        for r_client in rlist:
            rthread = threading.Thread(target=read, args=(r_client, requests, buffersize))
            rthread.start()
            #b_request = r_client.recv(buffersize)
            #requests.append(b_request)

        if requests:
            n_request = requests.pop()
            request = json.loads(n_request.decode(encoding))
            #request = requests.pop()
            if validate_request(request):
                action_name = request.get('action')
                controller = resolve(action_name)
                if controller:
                    try:
                        response = controller(request)
                    except Exception as err:
                        logging.error(f'Detected error: {err}')
                        response = make_response(request, 500, 'Internal server error')
                else:
                    logging.error(f'Detected error: Action not found, code 404')
                    response = make_response(request, 404, 'Action not found')
                w_mes = json.dumps(response)
                for w_client in wlist:
                    wthread = threading.Thread(target=write, args=(w_client, w_mes.encode(encoding)))
                    wthread.start()
                    #w_client.send(w_mes.encode(encoding))
            else:
                logging.error(f'Detected error: Wrong request, code 400')
                w_response = make_response(request, 400, 'Wrong request')
                mes = json.dumps(w_response)
                #print('mes: ', mes)
                for w_client in wlist:
                    wthread = threading.Thread(target=write, args=(w_client, mes.encode(encoding)))
                    wthread.start()
                    #w_client.send(mes)

except KeyboardInterrupt:
    pass
