import sys
from clinic.gui.yes_no_box import CustomDialog
from clinic.gui.add_update_gui import Add_update
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class UDSMessageBox(QMainWindow):
    def __init__(self,controller,phn,name,holder,parent):
        ''' initializes update, delete, setcur window'''
        super().__init__()
        if not holder:
            return
        self.setWindowTitle("Update Patient: %s" %name)
        self.parent = parent
        self.controller = controller
        self.phn = phn
        self.name = name


        # sets up lil doctor image 
        lil_doctor = QLabel()
        doc = QPixmap("clinic/gui/image_library/doctor_holding_board.png")
        lil_doctor.setPixmap(doc)

        # formatting update del setcur window with patient values
        patient = controller.search_patient(self.phn)
        entrytext1 = QLabel("You are Updating %s" %name)
        entrytext2 = QLabel("PHN: %s" %phn)
        entrytext3 = QLabel("Birthday: %s" %patient.birth_date)
        entrytext4 = QLabel("Phone number: %s" %patient.phone)
        entrytext5 = QLabel("Email: %s" %patient.email)
        entrytext6 = QLabel("Adress: %s" %patient.address)


        text1 = QLabel("Would you like to:")
        text2 = QLabel("UPDATE %s's information?" %name)
        text3 = QLabel("DELETE %s from the system?" %name)
        text4 = QLabel("SET %s as the CURRENT PATIENT?" %name)
        
        self.up_butn = QPushButton("Update")
        self.del_butn = QPushButton("Delete")
        self.cur_butn = QPushButton("Set")
        self.cancel_butn = QPushButton("Cancel")
        

        if self.is_current(): # changes the options if the viewed patient is the current patient
            self.up_butn.setEnabled(False)
            self.del_butn.setEnabled(False)
            self.cur_butn = QPushButton("Unset")
            text4 = QLabel("UNSET %s as the CURRENT PATIENT?" %name)

        #more layout
        layout1 = QHBoxLayout() 
        layout1.addWidget(self.up_butn)
        layout1.addWidget(self.del_butn)
        layout1.addWidget(self.cur_butn)
        layout1.addWidget(self.cancel_butn)

        butn_Widget = QWidget()
        butn_Widget.setLayout(layout1)

        layout2 = QVBoxLayout()
        layout2.addWidget(entrytext1)
        layout2.addWidget(entrytext2)
        layout2.addWidget(entrytext3)
        layout2.addWidget(entrytext4)
        layout2.addWidget(entrytext5)
        layout2.addWidget(entrytext6)


        layout6 = QVBoxLayout()
        layout6.addWidget(text1)
        layout6.addWidget(text2)
        layout6.addWidget(text3)
        layout6.addWidget(text4)

        questionwid = QWidget()
        questionwid.setLayout(layout6)
    
        wordwid = QWidget()
        wordwid.setLayout(layout2)

        layoutinfo = QVBoxLayout()
        layoutinfo.addWidget(wordwid)
        layoutinfo.addWidget(questionwid)
        
        layouttext = QWidget()
        layouttext.setLayout(layoutinfo)

        layout3 = QHBoxLayout()
        layout3.addWidget(layouttext)
        layout3.addWidget(lil_doctor)
        
        topwid = QWidget()
        topwid.setLayout(layout3)

        layout4 = QVBoxLayout()
        layout4.addWidget(topwid)
        layout4.addWidget(butn_Widget)

        mainwid = QWidget()
        mainwid.setLayout(layout4)


        self.setCentralWidget(mainwid)

        self.up_butn.clicked.connect(self.up_clicked)
        self.del_butn.clicked.connect(self.del_clicked)
        self.cur_butn.clicked.connect(self.cur_clicked)
        self.cancel_butn.clicked.connect(self.closeEvent)


    def up_clicked(self):
        ''' opens the update patient window'''
        patient = self.controller.search_patient(self.phn)
        self.update_box = Add_update(self.controller,"update",patient,parent = self)
        self.update_box.show()        

    def del_clicked(self):
        ''' deletes the viewed patient from the database and refreshes the table after confirmation '''
        askbox = CustomDialog("Delete Patient", "Are you sure you want to permanantly delete %s from the system?" %self.name)
        if askbox.exec():
            self.parent.patient_table.setEnabled(False)
            self.controller.delete_patient(self.phn)
            self.parent.refresh_table()
            self.parent.patient_table.setEnabled(True)
            self.closeEvent(self)


    def cur_clicked(self):
        ''' sets or unsets current patient'''
        if self.is_current(): # if current unsets it and provides a confirmation box
            self.controller.unset_current_patient()
            self.parent.parent.cur_patient()
            gmessage = QMessageBox()
            gmessage.setText("Current patient unset")
            gmessage.exec()
            self.close()
        else:
            self.controller.set_current_patient(self.phn) # if the viewed patient isnt the current patient then it will set the patient
            self.parent.parent.cur_patient()
            gmessage = QMessageBox()
            gmessage.setText("Current patient set to %s" %self.name)
            gmessage.exec()
            self.close()
            
    def is_current(self):
        ''' checks if the patient is the current patient '''
        cur_patient = self.controller.get_current_patient()
        if cur_patient is None:
            return False
        if cur_patient.phn == self.phn:
            return True
        else:
            return False

    def closer(self):
        ''' closes the window'''
        self.close()

    def closeEvent(self,event):
        ''' calls the closer which actually closes the window. This is connected to the x button on all windows'''
        self.closer()
    