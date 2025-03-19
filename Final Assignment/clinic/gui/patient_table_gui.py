from PyQt6.QtWidgets import *
from clinic.gui.patient_table_model import PatientTableModel
from clinic.gui.update_del_setcur import UDSMessageBox
from clinic.gui.add_update_gui import Add_update
from PyQt6.QtGui import *

class PatientTableGUI(QMainWindow):

    def __init__(self,controller,parent):
        '''
        Inializes the table of patients. Can be refreshed to show all patients, certain patients,
        and one patient.
        '''
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.set_cur_del = None

        #if controller is not logged into do not initialize table (security)
        if not self.controller.logged: 
            return
        
        self.setWindowTitle("Patients")
        self.resize(600, 400)
        self.parent = parent

        #creating widgets and setting layouts for this widget
        self.set_cur_del = UDSMessageBox(self.controller,"holder","holder",False,parent = self)
        self.patient_table = QTableView()
        self.patient_model = PatientTableModel(self.controller, parent = self)
        self.patient_table.setModel(self.patient_model)

        add_button = QPushButton("Create Patient")
        quit_button = QPushButton("Exit Patient List")

        self.patient_table.doubleClicked.connect(self.update_del_setcur)
        infotap = QLabel("Double click a patient to Update data")
        infotap.setFont(QFont('Arial', 12))

        self.patient_table.doubleClicked.connect(self.update_del_setcur)

        layout = QVBoxLayout()
        layout.addWidget(infotap)
        layout.addWidget(self.patient_table)
        layout.addWidget(add_button)
        layout.addWidget(quit_button)

        #connect buttons
        quit_button.clicked.connect(self.closeEvent)
        add_button.clicked.connect(self.add_patient)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)    
        self.refresh_table() 
        
    def refresh_table(self):
       '''
       Refreshes table with all patients in the system, calls method in table model
       '''
       self.patient_model.refresh_data()
       self.patient_table.setColumnWidth(1,150)
       self.patient_table.setColumnWidth(4,150)
       self.patient_table.setColumnWidth(5,150)


    def refresh_table_specific(self,info):      
       '''
       Refreshes table with patients in the info parameter (can be phn or search string)
       '''     
       self.patient_model.refresh_data_specific(info)

    def update_del_setcur(self):
        '''
        When table is double clicked, saves index and opens editor window to edit that current
        patient (set as current, delete, update) User choses command
        '''
        index = self.patient_table.selectionModel().currentIndex()
        self.current_patient_phn = int(index.sibling(index.row(), 0).data())
        self.current_patient_name = index.sibling(index.row(), 1).data()

        self.set_cur_del = UDSMessageBox(self.controller,self.current_patient_phn,self.current_patient_name,True,parent = self)
        self.set_cur_del.show()

    def add_patient(self):
        '''
        Opens a window that will recieve information and create a new patient in the system
        '''
        self.add_box = Add_update(self.controller,"create",None,parent=self)
        self.add_box.show()

    def closeEvent(self,event):
        '''
        Close the table and reset any buttons
        '''
        self.parent.list_all_butn.setEnabled(True)
        if self.set_cur_del:
            self.set_cur_del.close()
        self.close()
