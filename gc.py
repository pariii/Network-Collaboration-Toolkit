import socket
import time
import logging
import sys

HOST = raw_input('enter ip address: ')
PORT = 12000
TIMEOUT = 5
BUF_SIZE = 1024

class WhatsUpClient():

    def __init__(self, host=HOST, port=PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        logging.info('Connecting to %s:%s' % (host, port))
        while 1:
            try:
                buf = self.sock.recv(BUF_SIZE)
                sys.stdout.write(buf)
                cmd = raw_input()
                if str(cmd.strip()) == '!q':
                    self.sock.send(cmd.strip())
                    buf = self.sock.recv(BUF_SIZE)
                    sys.stdout.write(buf)
                    self.sock.close()
                self.sock.send(cmd)
            except:
                self.sock.close()

    def run(self):
        pass


def main():
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    client = WhatsUpClient()

if __name__ == '__main__':
    main()