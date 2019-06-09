import yaml
import socket
import json
import datetime
from argparse import ArgumentParser


parser = ArgumentParser(usage='python %(prog)s <ip address> [<port>]')
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
    'ip_address', type=str,
    help='Network interface to work server (IP address).'
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

try:
    sock = socket.socket()
    sock.connect((host, port))
    print('Client started')
    username = input('Enter your name: ')
    message = {
               "action": "presence",
               "time": str(datetime.datetime.now()),
                "type": "status",
                "user": {
                            "account_name": username,
                            "status": "Yep, I am here!"
                }

    }
    data = json.dumps(message)
    sock.send(data.encode(encoding))
    response = sock.recv(buffersize)
    answer = json.loads(response.decode(encoding))
    print(answer['response'])
    print(answer['alert'])
except KeyboardInterrupt:
    pass
