from PyQt6.QtWidgets import QVBoxLayout, QLabel, QDialog, QDialogButtonBox 

class CustomDialog(QDialog):
    def __init__(self, win_name, input_text):
        super().__init__()

        self.setWindowTitle(win_name)
        self.setFixedSize(300, 150)

        button_flags = (
            QDialogButtonBox.StandardButton.Yes | 
            QDialogButtonBox.StandardButton.No
        )

        self.buttonBox = QDialogButtonBox(button_flags)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        message = QLabel(input_text)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        
 