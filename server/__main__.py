import yaml
import socket
import json
from actions import resolve
from protocol import validate_request, make_response
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

        if validate_request(request):
            action_name = request.get('action')

            controller = resolve(action_name)
            if controller:
                try:
                    response = controller(request)
                except Exception as err:
                    print(err)
                    response = make_response(request, 500, 'Internal server error')
            else:
                response = make_response(request, 404, 'Action not found')
        else:
            make_response(request, 400, 'Wrong request')

        mes = json.dumps(response)
        client.send(mes.encode(encoding))
        client.close()
except KeyboardInterrupt:
    pass
