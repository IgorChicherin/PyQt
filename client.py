import socket
import pickle
import hmac
from enterprise import Company

class ClientConnection:
    def __init__(self, host, port):
        self.HOST, self.PORT = host, port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))

    def send_data(self, msg):
        msg = pickle.dumps(msg)
        self.sock.send(msg)
        self.responce = str(self.sock.recv(1024), 'utf-8')

    def client_auth(self, secret_key):
        while True:
            msg = self.sock.recv(1024)
            self.hash = hmac.new(secret_key, msg)
            self.digest = self.hash.digest()
            self.sock.send(self.digest)



    def __str__(self):
        return 'Recived {}'.format(self.responce)

    def __del__(self):
        self.sock.close()


if __name__ == '__main__':
    # company = {'name': 'ARK Group',
    #            'adress': 'some address',
    #            'inn': 12345678912,
    #            'email': 'some@email',
    #            'phone_number': 89281546474,
    #            'command': 'add'}
    # print(ClientConnection('localhost', 9000).send_data(company))
    msg = {'command': 'get', 'cls': Company, 'id': 1}
    ClientConnection('localhost', 9000).send_data(msg)

