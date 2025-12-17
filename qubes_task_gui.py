#!/usr/bin/env python3

import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, 
    QTableWidget, QTableWidgetItem, 
    QWidget, QProgressDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QThread, QTimer

class Worker(QObject):
    finished = pyqtSignal()
    packagesRetrieved = pyqtSignal(list)
    errorOccurred = pyqtSignal(str)

    def run(self):
        try:
            available_cmd = ['sudo', 'qubes-dom0-update', '--action=list', '3isec-qubes*']
            available_result = subprocess.run(available_cmd, capture_output=True, text=True)
            if available_result.returncode == 0:
                packages = available_result.stdout.strip().split('\n')[0:-1]
                self.packagesRetrieved.emit(packages)
            else:
                self.errorOccurred.emit("Failed to retrieve packages")
        except Exception as e:
            self.errorOccurred.emit(f"Error: {str(e)}")
        finally:
            self.finished.emit()

class WorkerThread(QThread):
    def __init__(self):
        super().__init__()
        self.worker = Worker()

    def run(self):
        self.worker.run()

class QubesPackageManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qubes Task List")
        self.resize(800, 600)

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.package_table = QTableWidget()
        self.package_table.setColumnCount(3)
        self.package_table.horizontalHeader().setStretchLastSection(True)
        self.package_table.setHorizontalHeaderLabels(['Package', 'Status', 'Description'])
        self.package_table.verticalHeader().setVisible(False)
        self.package_table.setColumnWidth(0, 300)
        self.package_table.setColumnWidth(1, 100)
        main_layout.addWidget(self.package_table)

        QTimer.singleShot(10, self.populate_package_list)

    def populate_package_list(self):
        self.progress_dialog = QProgressDialog("Fetching Task List", "Cancel", 0, 0, self)
        self.progress_dialog.setModal(True)
        self.progress_dialog.setWindowTitle("Tasks")
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()
        #self.progress_dialog.canceled.connect(self.close_application)

        # Create a worker thread
        self.worker_thread = WorkerThread()
        self.worker_thread.worker.packagesRetrieved.connect(self.update_package_list)
        self.worker_thread.worker.errorOccurred.connect(self.handle_error)
        self.worker_thread.finished.connect(self.progress_dialog.close)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    def update_package_list(self, packages):
        self.package_table.setRowCount(len(packages))
    
        status = "Installed"
        for row, package in enumerate(packages):
            if package.strip():
                trimmed_package = package.split('.')[0]
                if 'Installed packages' in trimmed_package:
                    trimmed_package = "Installed packages"
                if 'Available packages' in trimmed_package:
                    trimmed_package = "Available packages"
                    status = "Available"
                    status_item = QTableWidgetItem(status)
                package_item = QTableWidgetItem(trimmed_package)
                if 'packages' in trimmed_package :
                    package_item.setFlags(package_item.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable) 
                else:
                    package_item.setFlags(package_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.package_table.setItem(row, 0, package_item)

                status_item = QTableWidgetItem(status)
                status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable) 
                self.package_table.setItem(row, 1, status_item)
    
        self.statusBar().showMessage(f"Retrieved {len(packages)-2} packages", 5000)

        description_item = QTableWidgetItem("Description test")
        description_item.setFlags(package_item.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable) 

    #def close_application(self): 
        #if self.worker_thread.isRunning():
            #self.worker_thread.quit()
        #QApplication.quit()

    def handle_error(self, message):
        self.statusBar().showMessage(message, 5000)

def main():
    app = QApplication(sys.argv)
    window = QubesPackageManager()
    window.show()
    return app.exec()

if __name__ == '__main__':
    main()
