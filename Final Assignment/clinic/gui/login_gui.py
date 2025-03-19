import sys
from PyQt6.QtGui import QPixmap,QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QHBoxLayout, QVBoxLayout
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.gui.yes_no_box import CustomDialog


class LoginGUI(QWidget):
    def __init__(self,controller,parent):
        ''' initializes the login window'''
        super().__init__()
        self.controller = controller
        self.parent = parent
        layout1 = QVBoxLayout()
        layout2 = QGridLayout()

        self.logged_in = False


        # formatting 
        self.lil_doctor = QLabel()
        doc = QPixmap("clinic/gui/image_library/doctor_login.png")
        self.lil_doctor.setPixmap(doc)
        self.setStyleSheet("background-color: #333333;") 

        clinic = QLabel("Welcome to the Clinic!")
        clinic.setFont(QFont('Arial', 17))
        

        label_username = QLabel("Username")
        self.text_username = QLineEdit()
        self.text_username.setStyleSheet("background-color: #444444;") 

        label_password = QLabel("Password")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.text_password.setStyleSheet("background-color: #444444;") 

        self.button_login = QPushButton("Login")
        self.button_quit = QPushButton("Quit")
        self.button_login.setStyleSheet("background-color: #444444;") 
        self.button_quit .setStyleSheet("background-color: #444444;") 


        layout1.addWidget(self.lil_doctor)

        layout2.addWidget(clinic,0,1)
        layout2.addWidget(label_username,1,0)
        layout2.addWidget(self.text_username,1,1)
        layout2.addWidget(label_password,2,0)
        layout2.addWidget(self.text_password,2,1)
        layout2.addWidget(self.button_login,3,1)
        layout2.addWidget(self.button_quit,4,1)


        layout3 = QHBoxLayout()
        top_wid = QWidget()
        top_wid.setLayout(layout1)
        bot_wid = QWidget()
        bot_wid.setLayout(layout2)
        layout3.addWidget(top_wid)
        layout3.addWidget(bot_wid)
        self.setLayout(layout3)
        # connect the buttons' clicked signals to the slots below
        self.button_login.clicked.connect(self.login_button_clicked)
        self.button_quit.clicked.connect(self.quit_button_clicked)


    def login_button_clicked(self):
        ''' handles controller login '''

        #get the username and password from the widgets
        username = self.text_username.text()
        password = self.text_password.text()
        
        try:
            self.logged_in = self.controller.login(username,password)
            self.parent.main_search.create_table()
            self.parent.main_layout.setCurrentIndex(1)
            self.close()
        except (InvalidLoginException): #if the login isnt stored then it doesnt log you in 
            bmessage = QMessageBox()
            bmessage.setText("Wrong username or password.")
            retval = bmessage.exec()

        self.text_username.setText("")
        self.text_password.setText("")
        
        

    def quit_button_clicked(self):
        ''' quits window and all children after confirmation '''
        exit_mess = CustomDialog("Exit Clinic?","Are you sure you want to exit the Clinic?")
        if exit_mess.exec():
            for window in QApplication.topLevelWidgets():
                window.close()

    
    
    

