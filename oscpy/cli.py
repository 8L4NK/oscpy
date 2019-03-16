# coding: utf8
"""OSCPy command line tools"""

from argparse import ArgumentParser
from time import sleep
from sys import exit
from ast import literal_eval

from oscpy.client import send_message
from oscpy.server import OSCThreadServer


def _send(options):
    def _parse(s):
        try:
            return literal_eval(s)
        except:
            return s

    for i in range(options.repeat):
        send_message(
            options.address,
            [_parse(x) for x in options.message],
            options.host,
            options.port,
            safer=options.safer,
            encoding=options.encoding,
            encoding_errors=options.encoding_errors
        )


def _dump(options):
    def dump(address, *values):
        print('{}: {}'.format(address, values))

    osc = OSCThreadServer(
        encoding=options.encoding,
        encoding_errors=options.encoding_errors,
        default_handler=dump
    )
    osc.listen(
        address=options.host,
        port=options.port,
        default=True
    )
    while True:
        sleep(10)


def main():
    parser = ArgumentParser(description='OSCPy command line interface')

    subparser = parser.add_subparsers()

    send = subparser.add_parser('send', help='send an osc message to a server')
    send.set_defaults(func=_send)
    send.add_argument('--host', '-H', action='store', default='localhost',
                      help='host (ip or name) to send message to.')
    send.add_argument('--port', '-P', action='store', type=int, default='8000',
                      help='port to send message to.')
    send.add_argument('--encoding', '-e', action='store', default='utf-8',
                      help='how to encode the strings')
    send.add_argument('--encoding_errors', '-E', action='store', default='replace',
                      help='how to treat string encoding issues')
    send.add_argument('--safer', '-s', action='store_true',
                      help='wait a little after sending message')
    send.add_argument('--repeat', '-r', action='store', type=int, default=1,
                      help='how many times to send the message')

    send.add_argument('address', action='store',
                      help='OSC address to send the message to.')
    send.add_argument('message', nargs='*',
                        help='content of the message, separated by spaces.')

    dump = subparser.add_parser('dump', help='listen for messages and print them')
    dump.set_defaults(func=_dump)
    dump.add_argument('--host', '-H', action='store', default='localhost',
                      help='host (ip or name) to send message to.')
    dump.add_argument('--port', '-P', action='store', type=int, default='8000',
                      help='port to send message to.')
    dump.add_argument('--encoding', '-e', action='store', default='utf-8',
                      help='how to encode the strings')
    dump.add_argument('--encoding_errors', '-E', action='store', default='replace',
                      help='how to treat string encoding issues')

    # bridge = parser.add_parser('bridge', help='listen for messages and redirect them to a server')

    options = parser.parse_args()
    exit(options.func(options))