import qdarkstyle
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGraphicsObject)


class Ui_Screenshot(QGraphicsObject):

    def screenshotUi(self, Screenshot):
        self.screenshot = Screenshot
        Screenshot.setObjectName("Screenshot")
        Screenshot.setFixedSize(915, 520)
        Screenshot.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/browser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Screenshot.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Screenshot)
        self.centralwidget.setObjectName("centralwidget")
        self.preview = QtWidgets.QLabel(self.centralwidget)
        self.preview.setGeometry(QtCore.QRect(7, 14, 800, 480))
        self.preview.setFrameShape(QtWidgets.QFrame.Box)
        self.preview.setText("")
        self.preview.setObjectName("preview")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(814, 234, 74, 70))
        self.save.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save.setIcon(icon)
        self.save.setIconSize(QtCore.QSize(50, 50))
        self.save.setFlat(True)
        self.save.setObjectName("save")
        self.newImage = QtWidgets.QPushButton(self.centralwidget)
        self.newImage.setGeometry(QtCore.QRect(814, 144, 74, 70))
        self.newImage.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/add2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newImage.setIcon(icon2)
        self.newImage.setIconSize(QtCore.QSize(50, 50))
        self.newImage.setFlat(True)
        self.newImage.setObjectName("pushButton")
        Screenshot.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Screenshot)
        self.statusbar.setObjectName("statusbar")
        Screenshot.setStatusBar(self.statusbar)

        self.retranslateUi(Screenshot)
        QtCore.QMetaObject.connectSlotsByName(Screenshot)

        self.preview_screen = QApplication.primaryScreen().grabWindow(0, 440, 220, 800, 460)
        self.preview.setPixmap(self.preview_screen.scaled(800, 480,
                                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.save.clicked.connect(self.save_image)
        self.newImage.clicked.connect(self.new_image)

    def retranslateUi(self, Screenshot):
        _translate = QtCore.QCoreApplication.translate
        Screenshot.setWindowTitle(_translate("Screenshot", "screenshot"))

    def save_image(self):
        img, _ = QFileDialog.getSaveFileName(self.screenshot, "Salvar Arquivo",
                                             filter="PNG(*.png);; JPEG(*.jpg)")
        if img[-3:] == "png":
            self.preview_screen.save(img, "png")
        elif img[-3:] == "jpg":
            self.preview_screen.save(img, "jpg")

    def new_image(self):
        self.preview.setPixmap(self.preview_screen.scaled(800, 480,
                                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))

        QTimer.singleShot(1000, self.take_screenshot)
        self.screenshot.hide()

    def take_screenshot(self):
        self.preview_screen = QApplication.primaryScreen().grabWindow(0, 440, 220, 800, 460)
        self.preview.setPixmap(self.preview_screen.scaled(800, 480,
                                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.screenshot.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Screenshot = QtWidgets.QMainWindow()
    ui = Ui_Screenshot()
    ui.screenshotUi(Screenshot)
    Screenshot.show()
    sys.exit(app.exec_())
