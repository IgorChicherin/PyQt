import socket
import pickle
import hmac
import sys

from PyQt5 import QtWidgets, uic
from enterprise import Company
from enterprise import Employee

class ClientConnection:
    def __init__(self, host, port):
        self.HOST, self.PORT = host, port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))

    def send_data(self, msg, user):
        self.client_auth(user)
        msg = pickle.dumps(msg)
        self.sock.send(msg)
        self.responce = str(self.sock.recv(1024), 'utf-8')
        print('Recived {}'.format(self.responce))

    def client_auth(self, secret_key):
        msg = self.sock.recv(1024)
        self.hash = hmac.new(bytes(secret_key, 'utf-8'), msg)
        self.digest = self.hash.digest()
        self.sock.send(self.digest)

    def __del__(self):
        self.sock.close()


class ClientInterface(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('client.ui', self)
        self.exitButton.clicked.connect(QtWidgets.qApp.quit)
        self.runButton.clicked.connect(self.run)
        self.add_radioButton.clicked.connect(self.show_panel)

    def run(self):
        if self.comp_radioButton.isChecked():
            usr = self.login_lineEdit.displayText()
            if self.add_radioButton.isChecked() and usr:
                company = {'name': self.name_lineEdit.displayText(),
                           'adress': self.adress_lineEdit.displayText(),
                           'inn': self.inn_lineEdit.displayText(),
                           'email': self.email_lineEdit.displayText(),
                           'phone_number': self.phone_lineEdit.displayText(),
                           'command': 'add'}
                ClientConnection('localhost', 9000).send_data(company, usr)
            if self.del_radioButton.isChecked() and usr:
                payload = {'command': 'get', 'cls': Company}
                ClientConnection('localhost', 9000).send_data(payload, usr)

    def show_panel(self):
        self.setGeometry(300, 300, 804, 413)
        self.exitButton.setGeometry(700, 350, 91, 31)

if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # ex = ClientInterface()
    # ex.show()
    # sys.exit(app.exec_())
    payload = {'command': 'get', 'cls': Company, 'id': '1'}
    ClientConnection('localhost', 9000).send_data(payload, 'user')

