from PyQt6.QtWidgets import QMainWindow, QMessageBox,QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

class CreateNote(QMainWindow): 
    def __init__(self,controller,parent):
        '''
        Inializes the patient record for the current patient.
        '''
        super().__init__()
        self.controller = controller
        self.cur_patient = self.controller.get_current_patient()
        self.setWindowTitle("Create New Note")
        self.parent = parent

        #creation of widgets and layouts for the patient window
        self.input_box = QPlainTextEdit()
        self.input_box.setPlaceholderText("Insert note body here")
        create_butn = QPushButton("Create Note")
        cancel_butn = QPushButton("Cancel")

        lay1 = QHBoxLayout()
        lay1.addWidget(create_butn)
        lay1.addWidget(cancel_butn)
        butn_wid = QWidget()
        butn_wid.setLayout(lay1)

        lay2 = QVBoxLayout()
        lay2.addWidget(self.input_box)
        lay2.addWidget(butn_wid)
        totalwid = QWidget()
        totalwid.setLayout(lay2)

        self.setCentralWidget(totalwid)
        create_butn.clicked.connect(self.create_note)
        cancel_butn.clicked.connect(self.closeEvent)

    def create_note(self):
        '''
        Creates a new note for the patient and uploads it to the record
        '''
        text_body = self.input_box.toPlainText()
        if text_body == "":
            gmessage = QMessageBox()
            gmessage.setText("Please provide valid text input.")
            gmessage.exec()
            return
        
        self.controller.create_note(text_body)
        gmessage = QMessageBox()
        gmessage.setText("Note was created.")
        gmessage.exec()
        self.parent.list_all_notes()
        self.closeEvent(self)

    def closeEvent(self,event):
        '''closes window'''
        self.close()