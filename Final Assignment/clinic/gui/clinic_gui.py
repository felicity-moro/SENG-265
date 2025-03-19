import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QStackedLayout
from clinic.controller import Controller
from clinic.gui.login_gui import LoginGUI
from clinic.gui.search_main_gui import MainSearchGUI


class ClinicGUI(QMainWindow):

    def __init__(self):
        ''' initializes clinic gui'''
        super().__init__()
        #initializing the controller
        self.controller = Controller(True)
        self.setFixedSize(800, 500)
        
        self.main_layout = QStackedLayout()
        #setting up the main window and buttons
        self.setWindowTitle("Clinic")

        self.login_logout_screen = LoginGUI(self.controller, parent = self)
        self.main_search = MainSearchGUI(self.controller,parent = self)

        self.main_layout.addWidget(self.login_logout_screen)
        self.main_layout.addWidget(self.main_search)

        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)
        
    def closeEvent(self,event):
        ''' closes the window and all children of the window'''
        self.main_search.tear_table()
        for window in QApplication.topLevelWidgets():
                window.close()        

        
def main():
    ''' runs the application'''
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
