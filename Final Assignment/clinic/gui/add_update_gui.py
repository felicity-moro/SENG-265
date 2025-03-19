import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QGridLayout
from clinic.gui.yes_no_box import CustomDialog
from clinic.exception.illegal_operation_exception import IllegalOperationException



class Add_update(QMainWindow):
    def __init__(self,controller,type,patient,parent):
        ''' initializes the add update window'''
        super().__init__()
        self.type = type
        self.setWindowTitle("%s Patient"%self.type)
        self.parent = parent
        self.patient = patient
        self.controller = controller
        

        # foramts the window, also uses masks to limit input 
        welcome = QLabel("%s Patient:"%self.type)
        phn = QLabel("PHN")
        self.phn_edit = QLineEdit()
        if self.type == "update":
            self.phn_edit = QLineEdit(str(self.patient.phn))
        self.phn_edit.setInputMask("9999999999")

        name = QLabel("Name")
        self.name_edit = QLineEdit()
        if self.type == "update":
            self.name_edit = QLineEdit(self.patient.name)

        bday = QLabel("Birthdate")
        self.bday_edit = QLineEdit()
        if self.type == "update":
            self.bday_edit = QLineEdit(self.patient.birth_date)
        self.bday_edit.setInputMask("9999-99-99")

        phone = QLabel("Phone")
        self.phone_edit = QLineEdit()
        if self.type == "update":
            self.phone_edit = QLineEdit(self.patient.phone)
        self.phone_edit.setInputMask("999 999 9999")

        email = QLabel("Email")
        self.email_edit = QLineEdit()
        if self.type == "update":
            self.email_edit = QLineEdit(self.patient.email)

        address = QLabel("Address")
        self.address_edit = QLineEdit()
        if self.type == "update":
            self.address_edit = QLineEdit(self.patient.address)

        if self.type == "update":
            self.create_update_butn = QPushButton("Update Patient")
        else:
            self.create_update_butn = QPushButton("Create Patient")


        edit_layout = QGridLayout()
        edit_layout.addWidget(phn,0,0)
        edit_layout.addWidget(self.phn_edit,0,1)
        edit_layout.addWidget(name,1,0)
        edit_layout.addWidget(self.name_edit,1,1)
        edit_layout.addWidget(bday,2,0)
        edit_layout.addWidget(self.bday_edit,2,1)
        edit_layout.addWidget(phone,3,0)
        edit_layout.addWidget(self.phone_edit,3,1)
        edit_layout.addWidget(email,4,0)
        edit_layout.addWidget(self.email_edit,4,1)
        edit_layout.addWidget(address,5,0)
        edit_layout.addWidget(self.address_edit,5,1)

        edit_wid = QWidget()
        edit_wid.setLayout(edit_layout)

        total_layout = QVBoxLayout()
        total_layout.addWidget(welcome)
        total_layout.addWidget(edit_wid)
        total_layout.addWidget(self.create_update_butn)

        total_wid = QWidget()
        total_wid.setLayout(total_layout)
        self.setCentralWidget(total_wid)

        if self.type == "update":
            self.create_update_butn.clicked.connect(self.update_clicked)
        else:
            self.create_update_butn.clicked.connect(self.create_clicked)

    
    def update_clicked(self):
        ''' Updates the info if valid '''

        phn = self.phn_edit.text()
        name = self.name_edit.text()
        bday = self.bday_edit.text()
        phone = self.phone_edit.text()
        email = self.email_edit.text()
        address = self.address_edit.text()

        # wont update if any feilds are left blank
        if phn == "" or name == "" or name.isdigit() or bday == "" or phone == "" or email == "" or address == "":
            message = QMessageBox()
            message.setText("All fields must be filled out.")
            message.exec()
            return
        if len(phn) != 10 or len(phone) != 12 or len(bday) != 10: #reqiures proper format for some fields 
            message = QMessageBox()
            message.setText("PHN, phone number, or birth date are not completed.")
            message.exec()
            return

        try: # finalizes, closes window if there is no conflicts with phn
            self.controller.update_patient(self.patient.phn,int(phn),name,bday,phone,email,address)
            message = QMessageBox()
            message.setText("Patient has been updated.")
            message.exec()
            self.parent.parent.refresh_table()
            self.parent.closeEvent(self.parent)
            self.closeEvent(self)
            return

        except IllegalOperationException as exc:
            message = QMessageBox()
            message.setText("Cannot update patient's PHN to an existing PHN.")
            message.exec()
            return
        
    def create_clicked(self):
        ''' creates a new patient if valid '''
        phn = self.phn_edit.text()
        name = self.name_edit.text()
        bday = self.bday_edit.text()
        phone = self.phone_edit.text()
        email = self.email_edit.text()
        address = self.address_edit.text()

        # wont accept if any feilds are left blank
        if phn == "" or name == "" or bday == "" or name.isdigit() or phone == "" or email == "" or address == "":
            message = QMessageBox()
            message.setText("All fields must be filled out.")
            message.exec()
            return
        if len(phn) != 10 or len(phone) != 12 or len(bday) != 10: #reqiures proper format for some fields 
            message = QMessageBox()
            message.setText("PHN, phone number, or birth date are not completed.")
            message.exec()
            return

        try: # finalizes, closes window if there is no conflicts with phn
            self.controller.create_patient(int(phn),name,bday,phone,email,address)
            message = QMessageBox()
            message.setText("Patient has been created.")
            message.exec()
            try:
                self.parent.refresh_table()
            except:
                self.parent.patient_table.refresh_table()

            self.closeEvent(self)

            return
        except IllegalOperationException as exc:
            message = QMessageBox()
            message.setText("Cannot create a new patient with an existing PHN.")
            message.exec()
            return

    def closeEvent(self,event):
        ''' closes window. deals with alternative call origins.'''
        try:
            self.parent.list_all_butn.setEnabled(True)
        except:
            a=2
        self.close()


        