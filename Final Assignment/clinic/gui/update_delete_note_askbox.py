from PyQt6.QtWidgets import*
from clinic.gui.yes_no_box import CustomDialog

class UDNMessageBox(QMainWindow):
    def __init__(self,controller,type,cur_index,parent):
        '''
        Opens a window that asks for an index. Window can be either an update or 
        delete window, both ask for code of note to delete/update, if its an update window, 
        and the index exits, user will be able to update text. 
        '''
        super().__init__()
        self.setWindowTitle("%s Note" %type)
        self.type = type
        self.cur_index = cur_index
        self.parent = parent
        self.controller = controller
        self.code = None

        #initializing widgets and layouts for window
        ques = QLabel("Provide index to %s below:"%type.lower())
        self.ques_line = QLineEdit()
        if cur_index:
            self.ques_line.setText(str(cur_index))
        butn = QPushButton(type)
        cancel_butn = QPushButton("Cancel")
        cancel_butn2 = QPushButton("Cancel")
        self.text_box = QPlainTextEdit()
        self.text_box.setPlaceholderText("Write updated text here...")
        update_butn = QPushButton("Update Note")

        self.stack = QStackedLayout()

        lay1 = QHBoxLayout()
        lay1.addWidget(butn)
        lay1.addWidget(cancel_butn)
        wid1 = QWidget()
        wid1.setLayout(lay1)

        total_layout = QVBoxLayout()
        total_layout.addWidget(ques)
        total_layout.addWidget(self.ques_line)
        total_layout.addWidget(wid1)

        lay2 = QHBoxLayout()
        lay2.addWidget(update_butn)
        lay2.addWidget(cancel_butn2)
        wid2 = QWidget()
        wid2.setLayout(lay2)

        lay3 = QVBoxLayout()
        lay3.addWidget(self.text_box)
        lay3.addWidget(wid2)
        wid3 = QWidget()
        wid3.setLayout(lay3)

        topwid = QWidget()
        topwid.setLayout(total_layout)

        self.stack.addWidget(topwid)
        self.stack.addWidget(wid3)

        cent_wid = QWidget()
        cent_wid.setLayout(self.stack)

        self.setCentralWidget(cent_wid)

        #connect buttons to respective functions
        butn.clicked.connect(self.input_code)
        cancel_butn.clicked.connect(self.closeEvent)
        update_butn.clicked.connect(self.update_note)
        cancel_butn2.clicked.connect(self.closeEvent)


    def input_code(self):
        '''
        if the update/delete button is pressed, read given index and display if it exists. 
        Delete/updates note accordingly
        '''
        search_code = self.ques_line.text() 
        if not search_code.isdigit():
            gmessage = QMessageBox()
            gmessage.setText("Please provide a valid note index.")
            gmessage.exec()
            self.ques_line.setText("")
            return
        
        search_code = int(search_code)
        note = self.controller.search_note(search_code)
        if not note:
            gmessage = QMessageBox()
            gmessage.setText("Please provide a valid note index.")
            gmessage.exec()
            self.ques_line.setText("")
            return
        
        if self.type == "Update":
            self.stack.setCurrentIndex(1)
            self.code = search_code

        if self.type == "Delete":
            message = CustomDialog("Delete Note?","Are you sure you want to delete this note?")
            if message.exec():
                self.controller.delete_note(search_code)
                self.parent.clear_pressed()
                self.parent.list_all_notes()
                self.closeEvent(self)
            else:
                return

    def update_note(self):
        '''
        For and update note window, appears after a correct index was provided. Takes text from a text box
        and then updates the note.
        '''
        text = self.text_box.toPlainText()
        if text == "":
            gmessage = QMessageBox()
            gmessage.setText("Please provide valid text input.")
            gmessage.exec()
            return
        message = CustomDialog("Update Note?","Are you sure you want to update this note?")
        if message.exec():
            self.controller.update_note(self.code,text)
            self.parent.clear_pressed()
            self.parent.print_note(self.controller.search_note(self.code))
            self.closeEvent(self)
        else:
            return

    def closeEvent(self,event):
        '''
        Closes the askbox and resets buttons to be used in patient record
        '''
        self.parent.del_butn.setEnabled(True)
        self.parent.update_butn.setEnabled(True)
        self.close()