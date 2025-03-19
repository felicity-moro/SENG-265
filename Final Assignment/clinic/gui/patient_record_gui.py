from PyQt6.QtWidgets import *
from clinic.gui.update_delete_note_askbox import UDNMessageBox
from clinic.gui.create_note_gui import CreateNote

class PatientRecordTab(QMainWindow): 
    def __init__(self,controller,parent):
        '''
        Inializes the patient record window for the current patient.
        '''
        super().__init__()
        self.controller = controller
        self.cur_patient = self.controller.get_current_patient()
        self.setWindowTitle("%s's Record"%self.cur_patient.name)
        self.parent = parent
        self.cur_index = None
        self.input_box = None

        #creation of widgets and layouts for the patient window
        title_lab = QLabel("Patient Record:")
        pat_label = QLabel(self.cur_patient.__str__())
        unset_butn = QPushButton("Unset")
        ext_butn = QPushButton("Exit")
        
        retr_note = QLabel("Search note contents")
        self.retr_note_edit = QLineEdit()
        self.retr_note_edit.setPlaceholderText("Type desired text")
        retr_note_butn = QPushButton("Search")

        sear_note = QLabel("Search Note Index")
        self.sear_note_edit = QLineEdit()
        self.sear_note_edit.setPlaceholderText("Insert note index") 
        sear_note_butn = QPushButton("Search")

        list_all_butn = QPushButton("List All")
        self.add_butn = QPushButton("Create Note")
        self.del_butn = QPushButton("Delete Note")
        self.update_butn = QPushButton("Update Note") 

        self.note_box = QPlainTextEdit()
        self.note_box.setEnabled(False)


        lay1 = QVBoxLayout()
        lay1.addWidget(title_lab)
        lay1.addWidget(pat_label)
        lay1.addWidget(unset_butn)
        lay1.addWidget(ext_butn)
        wid1 = QWidget()
        wid1.setLayout(lay1)

        lay2 = QGridLayout()
        lay2.addWidget(retr_note,1,0)
        lay2.addWidget(self.retr_note_edit,1,1)
        lay2.addWidget(retr_note_butn,1,2)
        lay2.addWidget(sear_note,2,0)
        lay2.addWidget(self.sear_note_edit,2,1)
        lay2.addWidget(sear_note_butn,2,2)
        wid2 = QWidget()
        wid2.setLayout(lay2)

        lay3 = QVBoxLayout()
        lay3.addWidget(self.note_box)
        wid3 = QWidget()
        wid3.setLayout(lay3)

        lay4 = QHBoxLayout()
        lay4.addWidget(list_all_butn)
        lay4.addWidget(self.add_butn)
        lay4.addWidget(self.del_butn)
        lay4.addWidget(self.update_butn)
        wid4 = QWidget()
        wid4.setLayout(lay4)

        total_layout = QVBoxLayout()
        total_layout.addWidget(wid1)
        total_layout.addWidget(wid2)
        total_layout.addWidget(wid3)
        total_layout.addWidget(wid4)

        cent_wid = QWidget()
        cent_wid.setLayout(total_layout)

        self.setCentralWidget(cent_wid)

        #connect all buttons to respective functions
        unset_butn.clicked.connect(self.unset_cur_pat)
        ext_butn.clicked.connect(self.closeEvent)
        retr_note_butn.clicked.connect(self.retrieve_notes)
        sear_note_butn.clicked.connect(self.search_note)
        list_all_butn.clicked.connect(self.list_all_notes)
        self.add_butn.clicked.connect(self.create_note)
        self.del_butn.clicked.connect(self.delete_note_index)
        self.update_butn.clicked.connect(self.update_note_index)

    def unset_cur_pat(self):
        '''
        Unsets the current patient and then closes the current record
        '''
        self.controller.unset_current_patient()
        self.parent.cur_patient()
        gmessage = QMessageBox()
        gmessage.setText("Current patient unset.")
        gmessage.exec()
        self.closeEvent(self)
    
    def retrieve_notes(self):
        '''
        Retrieves a list of notes from patient record with a search string in respective qLineEdit then displays
        them in the textbox
        ''' 
        search_str = self.retr_note_edit.text() 
        if search_str == "":
            gmessage = QMessageBox()
            gmessage.setText("Please provide input text")
            gmessage.exec()
            return

        self.clear_pressed()
        notes_lst = self.controller.retrieve_notes(search_str)
        if len(notes_lst) == 0:
            gmessage = QMessageBox()
            gmessage.setText("No notes with that search input.")
            self.cur_index = None
            gmessage.exec()
            self.retr_note_edit.setText("")
            return
        if len(notes_lst) == 1:
            self.cur_index = notes_lst[0].code
        
        for note in notes_lst:
            self.print_note(note)

    
    def search_note(self):
        '''
        Retrieves a note via its code from patient record using the search string in a QLineEdit
        '''
        search_txt = self.sear_note_edit.text() 
        if not search_txt.isdigit():
            self.cur_index = None
            gmessage = QMessageBox()
            gmessage.setText("Please provide a valid note index.")
            gmessage.exec()
            self.sear_note_edit.setText("")
            return

        self.clear_pressed()
        search_code = int(search_txt)
        note = self.controller.search_note(search_code)
        if note is None:
            gmessage = QMessageBox()
            gmessage.setText("There is no note with index %d."%search_code)
            gmessage.exec()
            self.list_all_notes()
            return

        self.cur_index = search_code
        self.print_note(note)

    def clear_pressed(self):
        '''
        clears note box
        '''
        self.note_box.setPlainText("")

    def list_all_notes(self):
        '''
        lists all notes for the current patient and displays them in a textbox
        '''

        self.clear_pressed()
        notes_lst = self.controller.list_notes()

        for note in notes_lst:
            self.print_note(note)

    def create_note(self):
        '''
        Creates a new note for the patient and uploads it to the record, calls create note class
        '''
        self.input_box = CreateNote(self.controller,parent = self)
        self.input_box.show()

    def delete_note_index(self):
        '''
        Deletes note based off a given index or the current note in the textbox, calls update delete window
        '''
        self.update_butn.setEnabled(False)
        self.input_box = UDNMessageBox(self.controller,"Delete",self.cur_index,parent = self)
        self.input_box.show()

    def update_note_index(self):
        '''
        updates a note based off a given index or currentn note in the textbox, calls update delete window
        '''
        self.del_butn.setEnabled(False)
        self.input_box = UDNMessageBox(self.controller,"Update",self.cur_index,parent = self)
        self.input_box.show()

    def closeEvent(self,event):
        '''closes this window and child windows'''
        if self.input_box:
            self.input_box.closeEvent(self.input_box)
        self.close()

    def print_note(self,note):
        '''
        Prints a note to the textbox
        '''
        self.note_box.appendPlainText("Note %d, "%note.code)
        self.note_box.appendPlainText("%s\n"%str(note.timestamp))
        self.note_box.appendPlainText("%s\n"%note.text)
        self.note_box.appendPlainText("----END OF NOTE %d----\n"%note.code)