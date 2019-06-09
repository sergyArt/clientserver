import yaml
import socket
import json
from actions import resolve
from argparse import ArgumentParser


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


try:
    sock = socket.socket()

    sock.bind((host, port))
    sock.listen(5)
    print(f'Server was started with {host}:{port}')

    while True:
        client, address = sock.accept()
        print(f'Client was detected {address}')
        b_request = client.recv(buffersize)
        request = json.loads(b_request.decode(encoding))

        action_name = request.get('action')

        controller = resolve(action_name)

        response = controller(request)

        mes = json.dumps(response)
        client.send(mes.encode(encoding))
        client.close()
except KeyboardInterrupt:
    pass
