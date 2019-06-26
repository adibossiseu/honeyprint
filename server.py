# Copyright (C) 2013  Lukas Rist <glaslos@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from pkipplib import pkipplib
from gevent.server import StreamServer
from argparse import ArgumentParser


class PrintServer(object):

    def handle(self, sock, address):
        print('Handling connection from (%s)' % address)
        data = sock.recv(8192)
        print('Received (%s)' % repr(data))
        try:
            body = data.split('\r\n\r\n', 1)[1]
        except IndexError:
            body = data
        request = pkipplib.IPPRequest(body)
        request.parse()
        print('The request was (%s)' % request)
        request = pkipplib.IPPRequest(operation_id=pkipplib.CUPS_GET_DEFAULT)
        request.operation["attributes-charset"] = ("charset", "utf-8")
        request.operation["attributes-natural-language"] = ("naturalLanguage", "en-us")
        sock.send(request.dump())

    def get_server(self, host, port):
        connection = (host, port)
        server = StreamServer(connection, self.handle)
        print('LPR server started on: {0}'.format(connection))
        return server


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--host',
        dest='host',
        default='127.0.0.1',
        help='use this to specify the host to listen on'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=9100,
        help='use this to specify the port to listen on',
        dest='port'
    )
    args = parser.parse_args()

    ps = PrintServer()
    print_server = ps.get_server(args.host, args.port)
    print_server.serve_forever()


if __name__ == "__main__":
    main()
