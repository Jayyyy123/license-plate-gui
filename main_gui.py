"""
Author: YiJie
Email : yijie2333@gmail.com
Last edited: 2020.9.11
"""

from PyQt5 import QtWidgets

from gui_register import Ui_MainWindow


class App(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self,
                                                "Exit",
                                                "Are you sure you want to exit ?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        event.ignore()

        if result == QtWidgets.QMessageBox.Yes:
            event.accept()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App()
    ui.show()
    sys.exit(app.exec_())
