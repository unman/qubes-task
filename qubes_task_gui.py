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
        self.package_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.package_table.setColumnWidth(0, 300)
        self.package_table.setColumnWidth(1, 100)
        main_layout.addWidget(self.package_table)

        self.package_table.cellClicked.connect(self.show_package_info)
        QTimer.singleShot(10, self.populate_package_list)

    def init_description_column(self, pkg_count: int):
        placeholder = QTableWidgetItem("")
        placeholder.setFlags(placeholder.flags() & ~Qt.ItemFlag.ItemIsEditable)
        placeholder.setTextAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.package_table.setItem(0, 2, placeholder)

        if pkg_count > 1:
            self.package_table.setSpan(0, 2, pkg_count,  1)

    def populate_package_list(self):
        self.progress_dialog = QProgressDialog("Fetching Task List", "Cancel", 0, 0, self)
        self.progress_dialog.setModal(True)
        self.progress_dialog.setWindowTitle("Tasks")
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()
        self.progress_dialog.canceled.connect(self.cancel_and_quit)

        # Create a worker thread
        self.worker_thread = WorkerThread()
        self.worker_thread.worker.packagesRetrieved.connect(self.update_package_list)
        self.worker_thread.worker.errorOccurred.connect(self.handle_error)
        self.worker_thread.finished.connect(self.progress_dialog.hide)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    def update_package_list(self, packages):
        pkg_count = len(packages)
        self.package_table.setRowCount(pkg_count)
    
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
                if '3isec' in trimmed_package :
                    package_item.setFlags(package_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                else:
                    package_item.setFlags(package_item.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable) 
                self.package_table.setItem(row, 0, package_item)

                status_item = QTableWidgetItem(status)
                status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable) 
                self.package_table.setItem(row, 1, status_item)

        self.init_description_column(pkg_count)
    
        self.statusBar().showMessage(f"Retrieved {len(packages)-2} packages", 5000)

        description_item = QTableWidgetItem("")
        description_item.setFlags(package_item.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable) 

    def cancel_and_quit(self):
        if hasattr(self, "progress"):
            self.progress.close()
        if hasattr(self, "worker_thread"):
            self.worker_thread.terminate()
            self.worker_thread.wait()
        QApplication.instance().quit()

    def task_info(self, package):
        try:
            cmd = ['rpm','-qi',package]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.startswith('Summary'):
                        summary = line.split(':', 1)[1].strip()
                    elif line.startswith('Description'):
                        description_lines = []
                        for description_line in lines[lines.index(line)+1:]:
                            description_lines.append(description_line.strip())
                        description = '\n '.join(description_lines)
                return f"Summary: {summary}\nDescription: {description}"
            else:
                return f"No information"
        except Exception as e:
            return f"Failed to get information: {e}"

    def show_package_info(self, row, column):
        if column == 0:
            if self.package_table.item(row, 0) is not None:
                selected_package = self.package_table.item(row, 0).text()
                description = self.task_info(selected_package).strip()
            else:
                description = ""
            description_item = QTableWidgetItem(description)
            self.package_table.setItem(0, 2, description_item)

    def handle_error(self, message):
        self.statusBar().showMessage(message, 5000)

def main():
    app = QApplication(sys.argv)
    window = QubesPackageManager()
    window.show()
    return app.exec()

if __name__ == '__main__':
    main()
