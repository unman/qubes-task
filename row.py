# task_row.py
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QCheckBox, QHBoxLayout)


class TaskRowWidget(QWidget):

    def __init__(self, parent, name, summary):
        super(TaskRowWidget, self).__init__()
        self.parent = parent
        self.name = name # Name of widget used for searching.
        self.summary = summary 
        self.is_on = False 

        self.setAccessibleName = name
        self.lbl = QLabel(self.name)
        self.lbl2 = QLabel(self.summary)
        self.checked = QCheckBox("")
        self.checked.setAccessibleName(name)
        parent.taskGroup.addButton(self.checked)
        #self.checked.setStyleSheet("QCheckBox::indicator"
                                    #"{"
                                    #"background-color : lightgreen"
                                    #"}")
        self.btn_details = QPushButton("Details")
        self.btn_details.setAccessibleName(name)
        self.btn_details.setCheckable(False)
        self.btn_details.clicked.connect(parent.details_clicked)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.checked)
        self.hbox.addWidget(self.lbl,20)
        self.hbox.addWidget(self.lbl2,60)
        self.hbox.addWidget(self.btn_details)
        #self.hbox.addWidget(self.btn_install)
        self.setLayout(self.hbox)

