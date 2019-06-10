import yaml
import socket
import json
from datetime import datetime
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
    action = input('Enter action: ')
    data = input('Enter data: ')
    request = {
        'action': action,
        'data': data,
        'time': datetime.now().timestamp()
    }
    s_request = json.dumps(request)
    sock.send(s_request.encode(encoding))
    response = sock.recv(buffersize)
    answer = json.loads(response.decode(encoding))
    print(answer)
except KeyboardInterrupt:
    pass
