import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout

from clinic.controller import Controller

class LoginGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.setWindowTitle("Login")

        layout = QGridLayout()

        label_username = QLabel("Username")
        self.text_username = QLineEdit()
        label_password = QLabel("Password")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.button_login = QPushButton("Login")
        self.button_quit = QPushButton("Quit")

        layout.addWidget(label_username, 0, 0)
        layout.addWidget(self.text_username, 0, 1)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.text_password, 1, 1)
        layout.addWidget(self.button_login, 2, 0)
        layout.addWidget(self.button_quit, 2, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # connect the buttons' clicked signals to the slots below
        self.button_login.clicked.connect(self.login_button_clicked)
        self.button_quit.clicked.connect(self.quit_button_clicked)

    def login_button_clicked(self):
        ''' 'handles controller login '''

        # TODO: get the username and password from the widgets
        username = self.text_username.text()
        password = self.text_password.text()


        # TODO: login returns a boolean, so call controller.login() and create the
        # appropriate dialog message according to the value returned.
        # When you run your program, pick 'user' as username and '123456'
        # as password for a correct username/password combination.

        logged_in = self.controller.login(username,password)

        if logged_in:
            gmessage = QMessageBox()
            gmessage.setText("you have logged in")
            retval = gmessage.exec()
            self.quit_button_clicked()
        else:
            bmessage = QMessageBox()
            bmessage.setText("wrong username or password")
            retval = bmessage.exec()


        self.text_username.setText("")
        self.text_password.setText("")
        # TODO: after you finish the login, clear the text from the text widgets




    def quit_button_clicked(self):
        ''' quit the program '''
        # TODO: find the command to quit the program
        QApplication.quit()


app = QApplication(sys.argv)
window = LoginGUI()
window.show()
app.exec()