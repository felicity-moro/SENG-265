from PyQt6.QtCore import Qt, QAbstractTableModel

class PatientTableModel(QAbstractTableModel):
    '''
    Patient table model class, inherits from QAbstractTableModel, contains refresh functions to be used by gui.
    '''
    def __init__(self, controller,parent):
        '''
        initializes patient table for use of table gui
        '''
        super().__init__()
        self.controller = controller
        self.parent = parent

        self._data = []

    def refresh_data(self):
        '''
        refreshes data to display all patients in system then emits to the table gui
        '''
        self.reset()
        patient_matrix = []
        patient_info = self.controller.list_patients()

        for patient in patient_info:
            patient_lst = [str(patient.phn),patient.name,patient.birth_date,patient.phone,patient.email,patient.address]
            patient_matrix.append(patient_lst)
        self._data = patient_matrix
        self.layoutChanged.emit()

    def refresh_data_specific(self,info):
        '''
        refreshes data to display all patients in system that follow given parameter. 
        Will differentiate between a seach string and a PHN
        '''
        self.reset()
        patient_matrix = []

        if info.isdigit():
            patient = self.controller.search_patient(int(info))
            patient_lst = [patient.phn,patient.name,patient.birth_date,patient.phone,patient.email,patient.address]
            patient_matrix.append(patient_lst)
        else:
            patient_info = self.controller.retrieve_patients(info)
        
            for patient in patient_info:
                patient_lst = [patient.phn,patient.name,patient.birth_date,patient.phone,patient.email,patient.address]
                patient_matrix.append(patient_lst)
        
        self._data = patient_matrix
        self.layoutChanged.emit()

    def reset(self):
        '''
        Resets the data leaving the table blank
        '''
        self._data = []
        # emitting the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    def data(self, index, role):
        '''
        Formats data for the table
        '''
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, index):
        '''
        Returns row count of table
        '''
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        '''
        Returns column count of table
        '''
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        '''
        Sets up header titles for the table
        '''
        headers = ['PHN', 'Name', 'Birth Date', 'Phone', 'Email', 'Address']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)