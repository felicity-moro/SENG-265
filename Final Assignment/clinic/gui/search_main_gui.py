from clinic.gui.yes_no_box import CustomDialog
from clinic.gui.patient_table_gui import PatientTableGUI
from clinic.gui.add_update_gui import Add_update
from clinic.gui.patient_record_gui import PatientRecordTab
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import sys

class MainSearchGUI(QWidget):

    def __init__(self,controller,parent):
        ''' initializes the main search screen'''
        super().__init__()
        #initializing the controller and parent window
        self.controller = controller
        self.parent = parent
        self.patient_table = PatientTableGUI(self.controller,parent = self)
        self.setStyleSheet("background-color: #333333;") 

        #initializing layouts for the top part of the window that handles search and list all and image
        search_layout1 = QGridLayout()
        search_layout2 = QHBoxLayout()

        lil_doctor = QLabel()
        doc = QPixmap("clinic/gui/image_library/doctor_helping_patient.png")
        lil_doctor.setPixmap(doc)
        lil_doctor.adjustSize()
        lil_doctor.setFixedSize(lil_doctor.size())
        
        header = QLabel("The Clinic")
        header.setFont(QFont('Arial', 17))

        # formatting widget
        search_patient = QLabel("Search Patient")
        self.search_patient_text = QLineEdit()
        self.search_patient_text.setPlaceholderText("Enter full PHN or Patient Name")
        self.search_patient_text.setStyleSheet("background-color: #555555;") 
        self.search_butn = QPushButton("Search")
        self.search_butn.setStyleSheet("background-color: #444444;") 
        clear_butn = QPushButton("Clear")
        clear_butn.setStyleSheet("background-color: #444444;") 
        self.create_Patient = QPushButton("Create New Patient")
        self.create_Patient.setStyleSheet("background-color: #444444;") 
        self.list_all_butn = QPushButton("List All Patients")
        self.list_all_butn.setStyleSheet("background-color: #444444;") 
        logout_butn = QPushButton("Logout")
        quit_butn = QPushButton("Quit")

        #creating complete top half layout
        search_layout1.addWidget(header,0,0)
        search_layout1.addWidget(logout_butn,0,2)
        search_layout1.addWidget(quit_butn,1,2)
        search_layout1.addWidget(lil_doctor,2,1)
        search_layout1.addWidget(search_patient,3,0)
        search_layout1.addWidget(self.search_patient_text,3,1)
        search_layout1.addWidget(clear_butn,3,2)
        search_layout_top = QWidget()
        search_layout_top.setLayout(search_layout1)

        search_layout2.addWidget(self.search_butn)
        search_layout2.addWidget(self.create_Patient)
        search_layout2.addWidget(self.list_all_butn)
        search_layout_bot = QWidget()
        search_layout_bot.setLayout(search_layout2)

        search_layout = QVBoxLayout()
        search_layout.addWidget(search_layout_top)
        search_layout.addWidget(search_layout_bot)

        search_lay = QWidget()
        search_lay.setLayout(search_layout)

        #creating and initializing complete bottom half layout
        cur_pat_layout = QGridLayout()

        cur_pat = QLabel("Current Patient")
        self.cur_patient_text = QLineEdit()
        self.cur_patient_text.setEnabled(False)
        self.record_butn = QPushButton("See Current Patient's Record")
        self.record_butn.setEnabled(False)
    
        cur_pat_layout.addWidget(cur_pat,0,0)
        cur_pat_layout.addWidget(self.cur_patient_text,0,1)
        cur_pat_layout.addWidget(self.record_butn,1,1)

        cur_pat_lay = QWidget()
        cur_pat_lay.setLayout(cur_pat_layout)
        
        total_layout = QVBoxLayout()
        total_layout.addWidget(search_lay)
        total_layout.addWidget(cur_pat_lay)
    
        self.setLayout(total_layout)

        self.create_Patient.clicked.connect(self.add_patient)
        self.search_butn.clicked.connect(self.search_pressed)
        clear_butn.clicked.connect(self.search_clear_pressed)
        self.list_all_butn.clicked.connect(self.list_all_pressed)
        self.record_butn.clicked.connect(self.record_pressed)
        logout_butn.clicked.connect(self.logout_pressed)
        quit_butn.clicked.connect(self.quit_pressed) 
        

        #ADDED CODE:
        self.current_patient = None
        self.cur_patient_text.setEnabled(False)
        self.record_butn.setEnabled(False)
        
    def cur_patient(self): #ADDED
        ''' sets the current patient from the controller'''
        self.current_patient = self.controller.get_current_patient()

        # sets the info bar in the bottom of search main to the current patients phn and name if they are set
        if self.current_patient is None:
            self.record_butn.setEnabled(False)
            self.cur_patient_text.setText("") 
        else:
            self.record_butn.setEnabled(True)
            self.cur_patient_text.setText(str(self.current_patient.phn) + " - " + self.current_patient.name)

        try:
            self.cur_record.close() 
        except:
            return
            

    def record_pressed(self): 
        '''Shows the record window'''
        self.cur_record = PatientRecordTab(self.controller,parent = self)
        self.cur_record.show()

    def search_clear_pressed(self):
        '''Clears the search bar'''
        self.search_patient_text.setText("")

    #CHANGED THE FORMATTING OF THIS FUNCTION TO INCLUDE NUMBERS IN NAMES I GUESS AND TO SHOW PATIENT IN TABLE
    def search_pressed(self):
        '''Uses the search bar to return all patients with a letter or a specified PHN'''
        text = self.search_patient_text.text()
        text = text.strip()

        if text.isdigit(): # first checks if the input text is a digit
            phn = int(text)
            patient = self.controller.search_patient(phn) 
            if patient is None:
                patient_list = self.controller.retrieve_patients(text)
                if len(patient_list) == 0: # needs to have a valid search input 
                    gmessage = QMessageBox()
                    gmessage.setText("There are no patients with this name or PHN.")
                    self.list_all_butn.setEnabled(False) # stops the user from having multiple listings open 
                    gmessage.exec()
                    return
                self.patient_table.setEnabled(False) 
                self.patient_table.refresh_table_specific(text) 
                self.patient_table.show()
                self.patient_table.setEnabled(True)

            else: #reloads the table info
                self.tear_table()
                self.create_table()
                self.patient_table.refresh_table_specific(text)
                self.patient_table.show()
                

                #open patient window
        else:
            #retrieve patients name via string and not a number/phn
            patient_list = self.controller.retrieve_patients(text)
            if len(patient_list) == 0 :# needs to have a valid search input 
                gmessage = QMessageBox() 
                gmessage.setText("There are no patients with this name or PHN.")
                self.list_all_butn.setEnabled(False)
                gmessage.exec()
                return
            
            #resets table 
            self.patient_table.setEnabled(False) 
            self.patient_table.refresh_table_specific(text)
            self.patient_table.show()
            self.patient_table.setEnabled(True)


    def list_all_pressed(self):
        ''' displays patient table'''
        self.patient_table.refresh_table()
        self.patient_table.show()

    def logout_pressed(self):
        ''' logs out and goes to main screen after confirmation'''
        exit_mess = CustomDialog("Logout","Are you sure you want to Logout?")
        if exit_mess.exec():
            self.close_tabs()
            self.tear_table()
            self.controller.logout()
            self.parent.main_layout.setCurrentIndex(0)

    def quit_pressed(self):
        ''' Ends session. Closes window after confimation'''
        exit_mess = CustomDialog("Exit Clinic?","Are you sure you want to exit the Clinic?")
        if exit_mess.exec():
            self.controller.logout()
            for window in QApplication.topLevelWidgets():
                window.close()
    
    def create_table(self):
        ''' creates patient table window'''
        self.patient_table = PatientTableGUI(self.controller,parent = self)

    def tear_table(self):
        ''' closes the table, sets it to none. helper function'''
        if self.patient_table:
            self.patient_table.close()
        self.patient_table = None

    def close_tabs(self):
        ''' closes the table '''
        if self.patient_table:
            self.patient_table.close()

    def add_patient(self):
        ''' uses add_update ui gui '''
        self.add_box = Add_update(self.controller,"create",None,parent=self)
        self.add_box.show()
        
  

            
