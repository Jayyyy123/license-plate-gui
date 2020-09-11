import argparse
import datetime
import time
import webbrowser

import cv2
import mysql.connector
import numpy as np
import pymysql
import pyperclip
import pytesseract
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from imutils.object_detection import non_max_suppression

import product2
from gui_overview import Ui_Overview
from gui_signup import Ui_signup

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

__appname__ = 'license-plate-gui'


def show_empty_popup():
    message = QMessageBox()
    message.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    message.setWindowTitle("Hi")
    message.setText("VVIP is empty, please proceed.")
    message.setIcon(QMessageBox.Information)
    message.exec_()


def show_full_popup():
    message = QMessageBox()
    message.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    message.setWindowTitle("Oops")
    message.setText("VVIP is full, please proceed to next.")
    message.setIcon(QMessageBox.Information)
    message.exec_()


def show_inserted_popup():
    message = QMessageBox()
    message.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    message.setWindowTitle("Success")
    message.setText("Data is successfully inserted.")
    message.setIcon(QMessageBox.Information)
    message.exec_()


def duplicate_entry():
    message = QMessageBox()
    message.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    message.setWindowTitle("Oops!")
    message.setText("Duplicate ID, please retry.")
    message.setIcon(QMessageBox.Information)
    message.exec_()


def contact_me():
    webbrowser.open('https://github.com/Jayyyy123')


def about():
    webbrowser.open('https://en.wikipedia.org/wiki/Automatic_number-plate_recognition')


def aboutQt():
    webbrowser.open('https://doc.qt.io/qt-5/qtdesigner-manual.html')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.window = MainWindow
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(1500, 920)
        MainWindow.showMaximized()
        MainWindow.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/car.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SiteCombox = QtWidgets.QComboBox(self.centralwidget)
        self.SiteCombox.setGeometry(QtCore.QRect(50, 140, 290, 25))
        self.SiteCombox.setFont(font)
        self.SiteCombox.setObjectName("SiteCombox")
        self.SiteCombox.addItem("")
        self.SiteLabel = QtWidgets.QLabel(self.centralwidget)
        self.SiteLabel.setGeometry(QtCore.QRect(52, 122, 47, 13))
        self.SiteLabel.setFont(font)
        self.SiteLabel.setObjectName("SiteLabel")
        self.icon = QtWidgets.QLabel(self.centralwidget)
        self.icon.setGeometry(QtCore.QRect(66, 42, 61, 55))
        self.icon.setFont(font)
        self.icon.setAutoFillBackground(False)
        self.icon.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.icon.setText("")
        self.icon.setPixmap(QtGui.QPixmap("icon/car.png"))
        self.icon.setScaledContents(True)
        self.icon.setObjectName("icon")
        self.VVIPSpaceLeft = QtWidgets.QLabel(self.centralwidget)
        self.VVIPSpaceLeft.setGeometry(QtCore.QRect(272, 224, 68, 16))
        self.VVIPSpaceLeft.setFont(font)
        self.VVIPSpaceLeft.setObjectName("VVIPSpaceLeft")
        self.VisitorsSpaceLeft = QtWidgets.QLabel(self.centralwidget)
        self.VisitorsSpaceLeft.setGeometry(QtCore.QRect(272, 506, 68, 16))
        self.VisitorsSpaceLeft.setFont(font)
        self.VisitorsSpaceLeft.setObjectName("VisitorsSpaceLeft")
        self.SpecialNeedbar = QtWidgets.QProgressBar(self.centralwidget)
        self.SpecialNeedbar.setGeometry(QtCore.QRect(50, 322, 280, 10))
        self.SpecialNeedbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())
        self.SpecialNeedbar.setProperty("value", 0)
        self.SpecialNeedbar.setAlignment(QtCore.Qt.AlignCenter)
        self.SpecialNeedbar.setTextVisible(True)
        self.SpecialNeedbar.setMaximum(100)
        self.SpecialNeedbar.setObjectName("SpecialNeedBtnbar")
        self.Visitorsbar = QtWidgets.QProgressBar(self.centralwidget)
        self.Visitorsbar.setGeometry(QtCore.QRect(50, 530, 280, 10))
        self.Visitorsbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())
        self.Visitorsbar.setProperty("value", 0)
        self.Visitorsbar.setAlignment(QtCore.Qt.AlignCenter)
        self.Visitorsbar.setTextVisible(True)
        self.Visitorsbar.setMaximum(100)
        self.Visitorsbar.setObjectName("Visitorsbar")
        self.VVIPLabel = QtWidgets.QLabel(self.centralwidget)
        self.VVIPLabel.setGeometry(QtCore.QRect(40, 190, 300, 70))
        self.VVIPLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.VVIPLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.VVIPLabel.setText("")
        self.VVIPLabel.setObjectName("VVIPLabel")
        self.ZoneBLabel = QtWidgets.QLabel(self.centralwidget)
        self.ZoneBLabel.setGeometry(QtCore.QRect(40, 406, 300, 70))
        self.ZoneBLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.ZoneBLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.ZoneBLabel.setText("")
        self.ZoneBLabel.setObjectName("ZoneBLabel")
        self.ZoneBSpaceLeft = QtWidgets.QLabel(self.centralwidget)
        self.ZoneBSpaceLeft.setGeometry(QtCore.QRect(272, 436, 68, 16))
        self.ZoneBSpaceLeft.setFont(font)
        self.ZoneBSpaceLeft.setObjectName("ZoneBSpaceLeft")
        self.VVIPPercentageOccupied = QtWidgets.QLabel(self.centralwidget)
        self.VVIPPercentageOccupied.setGeometry(QtCore.QRect(48, 222, 94, 18))
        self.VVIPPercentageOccupied.setFont(font)
        self.VVIPPercentageOccupied.setObjectName("VVIPPercentageOccupied")
        self.ZoneAPercentageOccupied = QtWidgets.QLabel(self.centralwidget)
        self.ZoneAPercentageOccupied.setGeometry(QtCore.QRect(48, 368, 94, 18))
        self.ZoneAPercentageOccupied.setFont(font)
        self.ZoneAPercentageOccupied.setObjectName("ZoneAPercentageOccupied")
        self.ZoneBPercentageOccupied = QtWidgets.QLabel(self.centralwidget)
        self.ZoneBPercentageOccupied.setGeometry(QtCore.QRect(48, 434, 94, 18))
        self.ZoneBPercentageOccupied.setFont(font)
        self.ZoneBPercentageOccupied.setObjectName("ZoneBPercentageOccupied")
        self.SpecialNeedPercentageOccupied = QtWidgets.QLabel(self.centralwidget)
        self.SpecialNeedPercentageOccupied.setGeometry(QtCore.QRect(48, 300, 94, 18))
        self.SpecialNeedPercentageOccupied.setFont(font)
        self.SpecialNeedPercentageOccupied.setObjectName("SpecialNeedPercentageOccupied")
        self.VisitorsPercentageOccupied = QtWidgets.QLabel(self.centralwidget)
        self.VisitorsPercentageOccupied.setGeometry(QtCore.QRect(48, 506, 94, 18))
        self.VisitorsPercentageOccupied.setFont(font)
        self.VisitorsPercentageOccupied.setObjectName("VisitorsPercentageOccupied")
        self.ZoneASpaceLeft = QtWidgets.QLabel(self.centralwidget)
        self.ZoneASpaceLeft.setGeometry(QtCore.QRect(272, 370, 68, 16))
        self.ZoneASpaceLeft.setFont(font)
        self.ZoneASpaceLeft.setObjectName("ZoneASpaceLeft")
        self.SpecialNeedSpaceLeft = QtWidgets.QLabel(self.centralwidget)
        self.SpecialNeedSpaceLeft.setGeometry(QtCore.QRect(272, 302, 68, 16))
        self.SpecialNeedSpaceLeft.setFont(font)
        self.SpecialNeedSpaceLeft.setObjectName("SpecialNeedSpaceLeft")
        self.ZoneAbar = QtWidgets.QProgressBar(self.centralwidget)
        self.ZoneAbar.setGeometry(QtCore.QRect(50, 392, 280, 10))
        self.ZoneAbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())
        self.ZoneAbar.setProperty("value", 0)
        self.ZoneAbar.setAlignment(QtCore.Qt.AlignCenter)
        self.ZoneAbar.setTextVisible(True)
        self.ZoneAbar.setMaximum(100)
        self.ZoneAbar.setObjectName("ZoneAbar")
        self.ZoneALabel = QtWidgets.QLabel(self.centralwidget)
        self.ZoneALabel.setGeometry(QtCore.QRect(40, 338, 300, 70))
        self.ZoneALabel.setFrameShape(QtWidgets.QFrame.Box)
        self.ZoneALabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.ZoneALabel.setText("")
        self.ZoneALabel.setObjectName("ZoneALabel")
        self.VVIPOpenIcon = QtWidgets.QLabel(self.centralwidget)
        self.VVIPOpenIcon.setGeometry(QtCore.QRect(255, 204, 50, 16))
        self.VVIPOpenIcon.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.VVIPOpenIcon.setText("")
        self.VVIPOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
        self.VVIPOpenIcon.setScaledContents(True)
        self.VVIPOpenIcon.setObjectName("VVIPOpenIcon")
        self.SpecialNeedOpenIcon = QtWidgets.QLabel(self.centralwidget)
        self.SpecialNeedOpenIcon.setGeometry(QtCore.QRect(255, 282, 50, 16))
        self.SpecialNeedOpenIcon.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SpecialNeedOpenIcon.setText("")
        self.SpecialNeedOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
        self.SpecialNeedOpenIcon.setScaledContents(True)
        self.SpecialNeedOpenIcon.setObjectName("SpecialNeedOpenIcon")
        self.ZoneAOpenIcon = QtWidgets.QLabel(self.centralwidget)
        self.ZoneAOpenIcon.setGeometry(QtCore.QRect(255, 348, 50, 16))
        self.ZoneAOpenIcon.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ZoneAOpenIcon.setText("")
        self.ZoneAOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
        self.ZoneAOpenIcon.setScaledContents(True)
        self.ZoneAOpenIcon.setObjectName("ZoneAOpenIcon")
        self.ZoneBOpenIcon = QtWidgets.QLabel(self.centralwidget)
        self.ZoneBOpenIcon.setGeometry(QtCore.QRect(255, 416, 50, 16))
        self.ZoneBOpenIcon.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ZoneBOpenIcon.setText("")
        self.ZoneBOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
        self.ZoneBOpenIcon.setScaledContents(True)
        self.ZoneBOpenIcon.setObjectName("ZoneBOpenIcon")
        self.VisitorsOpenIcon = QtWidgets.QLabel(self.centralwidget)
        self.VisitorsOpenIcon.setGeometry(QtCore.QRect(255, 482, 50, 16))
        self.VisitorsOpenIcon.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.VisitorsOpenIcon.setText("")
        self.VisitorsOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
        self.VisitorsOpenIcon.setScaledContents(True)
        self.VisitorsOpenIcon.setObjectName("VisitorsOpenIcon")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.clock = QtWidgets.QLabel(self.centralwidget)
        self.clock.setGeometry(QtCore.QRect(1530, 28, 100, 20))
        self.clock.setFont(font)
        self.clock.setObjectName("Clock")
        self.RegistrationLabel = QtWidgets.QLabel(self.centralwidget)
        self.RegistrationLabel.setGeometry(QtCore.QRect(440, 74, 334, 40))
        self.RegistrationLabel.setFont(font)
        self.RegistrationLabel.setObjectName("RegistrationLabel")
        self.UploadedDataImage = QtWidgets.QLabel(self.centralwidget)
        self.UploadedDataImage.setGeometry(QtCore.QRect(436, 638, 650, 250))
        self.UploadedDataImage.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.UploadedDataImage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.UploadedDataImage.setFrameShadow(QtWidgets.QFrame.Plain)
        self.UploadedDataImage.setText("")
        self.UploadedDataImage.setObjectName("UploadedDataImage")
        img = "./parking_lot.PNG"
        pixmap = QPixmap(img)
        pixmapResize = pixmap.scaled(650, 250)
        self.UploadedDataImage.setPixmap(pixmapResize)
        self.SPSlabel = QtWidgets.QLabel(self.centralwidget)
        self.SPSlabel.setGeometry(QtCore.QRect(580, 900, 320, 25))
        self.SPSlabel.setObjectName("SPSlabel")
        self.StatusText = QtWidgets.QLabel(self.centralwidget)
        self.StatusText.setGeometry(QtCore.QRect(1130, 82, 68, 26))
        self.StatusText.setFont(font)
        self.StatusText.setObjectName("StatusText")
        status_font = QtGui.QFont()
        status_font.setFamily("Consolas")
        status_font.setPointSize(12)
        status_font.setBold(True)
        status_font.setWeight(75)
        self.Status = QtWidgets.QTextEdit(self.centralwidget)
        self.Status.setGeometry(QtCore.QRect(1130, 110, 370, 420))
        self.Status.setObjectName("Status")
        self.Status.setFont(status_font)
        self.Status.setReadOnly(True)
        self.VehiclePlateText = QtWidgets.QLabel(self.centralwidget)
        self.VehiclePlateText.setGeometry(QtCore.QRect(1130, 618, 184, 22))
        self.VehiclePlateText.setFont(font)
        self.VehiclePlateText.setObjectName("VehiclePlateText")
        self.VehiclePlateTextImage = QtWidgets.QLabel(self.centralwidget)
        self.VehiclePlateTextImage.setGeometry(QtCore.QRect(1130, 738, 184, 22))
        self.VehiclePlateTextImage.setFont(font)
        self.VehiclePlateTextImage.setObjectName("VehiclePlateTextImage")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Options = QtWidgets.QComboBox(self.centralwidget)
        self.Options.setGeometry(QtCore.QRect(1140, 546, 150, 28))
        self.Options.setFont(font)
        self.Options.setObjectName("Options")
        self.Options.addItem("")
        self.UploadedDataLabel = QtWidgets.QLabel(self.centralwidget)
        self.UploadedDataLabel.setGeometry(QtCore.QRect(442, 612, 220, 22))
        self.UploadedDataLabel.setFont(font)
        self.UploadedDataLabel.setObjectName("UploadedDataLabel")
        self.CarImage = QtWidgets.QLabel(self.centralwidget)
        self.CarImage.setGeometry(QtCore.QRect(436, 110, 660, 420))
        self.CarImage.setStyleSheet("border: 1px solid light blue;")
        self.CarImage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.CarImage.setText("")
        self.CarImage.setObjectName("CarImage")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(38, 582, 350, 310))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setPlaceholderText("You can write text here.\n")
        self.plainTextEdit.setFont(font)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.ParkingNavigation = QtWidgets.QComboBox(self.centralwidget)
        self.ParkingNavigation.setGeometry(QtCore.QRect(144, 60, 140, 25))
        self.ParkingNavigation.setFont(font)
        self.ParkingNavigation.setEditable(False)
        self.ParkingNavigation.setFrame(False)
        self.ParkingNavigation.setObjectName("ParkingNavigation")
        self.ParkingNavigation.addItem("")
        self.ZoneBbar = QtWidgets.QProgressBar(self.centralwidget)
        self.ZoneBbar.setGeometry(QtCore.QRect(50, 460, 280, 10))
        self.ZoneBbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())
        self.ZoneBbar.setProperty("value", 0)
        self.ZoneBbar.setTextVisible(True)
        self.ZoneBbar.setMaximum(100)
        self.ZoneBbar.setObjectName("ZoneBbar")
        self.VVIParrow = QtWidgets.QLabel(self.centralwidget)
        self.VVIParrow.setGeometry(QtCore.QRect(314, 204, 16, 16))
        self.VVIParrow.setFont(font)
        self.VVIParrow.setText("")
        self.VVIParrow.setPixmap(QtGui.QPixmap("./icon/arrow2.png"))
        self.VVIParrow.setScaledContents(True)
        self.VVIParrow.setObjectName("VVIParrow")
        self.VVIPText = QtWidgets.QLabel(self.centralwidget)
        self.VVIPText.setGeometry(QtCore.QRect(60, 196, 110, 29))
        self.VVIPText.setFont(font)
        self.VVIPText.setObjectName("VVIPText")
        self.VisitorsLabel = QtWidgets.QLabel(self.centralwidget)
        self.VisitorsLabel.setGeometry(QtCore.QRect(40, 474, 300, 73))
        self.VisitorsLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.VisitorsLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.VisitorsLabel.setText("")
        self.VisitorsLabel.setObjectName("VisitorsLabel")
        self.SpecialNeedText = QtWidgets.QLabel(self.centralwidget)
        self.SpecialNeedText.setGeometry(QtCore.QRect(60, 272, 125, 29))
        self.SpecialNeedText.setFont(font)
        self.SpecialNeedText.setObjectName("SpecialNeedText")
        self.VisitorsText = QtWidgets.QLabel(self.centralwidget)
        self.VisitorsText.setGeometry(QtCore.QRect(60, 478, 78, 27))
        self.VisitorsText.setFont(font)
        self.VisitorsText.setObjectName("VisitorsText")
        self.SpecialNeedLabel = QtWidgets.QLabel(self.centralwidget)
        self.SpecialNeedLabel.setGeometry(QtCore.QRect(40, 270, 300, 70))
        self.SpecialNeedLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.SpecialNeedLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.SpecialNeedLabel.setText("")
        self.SpecialNeedLabel.setObjectName("SpecialNeedLabel")
        self.VVIPbar = QtWidgets.QProgressBar(self.centralwidget)
        self.VVIPbar.setGeometry(QtCore.QRect(50, 242, 280, 10))
        self.VVIPbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())
        self.VVIPbar.setProperty("value", 0)
        self.VVIPbar.setAlignment(QtCore.Qt.AlignCenter)
        self.VVIPbar.setTextVisible(True)
        self.VVIPbar.setMaximum(100)
        self.VVIPbar.setObjectName("VVIPbar")
        self.ZoneText = QtWidgets.QLabel(self.centralwidget)
        self.ZoneText.setGeometry(QtCore.QRect(60, 410, 71, 25))
        self.ZoneText.setFont(font)
        self.ZoneText.setObjectName("ZoneText")
        self.ZoneAText = QtWidgets.QLabel(self.centralwidget)
        self.ZoneAText.setGeometry(QtCore.QRect(60, 340, 71, 27))
        self.ZoneAText.setFont(font)
        self.ZoneAText.setObjectName("ZoneAText")
        self.SpecialNeedarrow = QtWidgets.QLabel(self.centralwidget)
        self.SpecialNeedarrow.setGeometry(QtCore.QRect(314, 282, 16, 16))
        self.SpecialNeedarrow.setFont(font)
        self.SpecialNeedarrow.setText("")
        self.SpecialNeedarrow.setPixmap(QtGui.QPixmap("./icon/arrow2.png"))
        self.SpecialNeedarrow.setScaledContents(True)
        self.SpecialNeedarrow.setObjectName("SpecialNeedarrow")
        self.ZoneAarrow = QtWidgets.QLabel(self.centralwidget)
        self.ZoneAarrow.setGeometry(QtCore.QRect(314, 348, 16, 16))
        self.ZoneAarrow.setFont(font)
        self.ZoneAarrow.setText("")
        self.ZoneAarrow.setPixmap(QtGui.QPixmap("./icon/arrow2.png"))
        self.ZoneAarrow.setScaledContents(True)
        self.ZoneAarrow.setObjectName("ZoneAarrow")
        self.ZoneBarrow = QtWidgets.QLabel(self.centralwidget)
        self.ZoneBarrow.setGeometry(QtCore.QRect(314, 416, 16, 16))
        self.ZoneBarrow.setFont(font)
        self.ZoneBarrow.setText("")
        self.ZoneBarrow.setPixmap(QtGui.QPixmap("./icon/arrow2.png"))
        self.ZoneBarrow.setScaledContents(True)
        self.ZoneBarrow.setObjectName("ZoneBarrow")
        self.Visitorsarrow = QtWidgets.QLabel(self.centralwidget)
        self.Visitorsarrow.setGeometry(QtCore.QRect(314, 482, 16, 16))
        self.Visitorsarrow.setFont(font)
        self.Visitorsarrow.setText("")
        self.Visitorsarrow.setPixmap(QtGui.QPixmap("./icon/arrow2.png"))
        self.Visitorsarrow.setScaledContents(True)
        self.Visitorsarrow.setObjectName("Visitorsarrow_")
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.VehiclePlateNumberImage = QtWidgets.QLabel(self.centralwidget)
        self.VehiclePlateNumberImage.setGeometry(QtCore.QRect(1130, 646, 282, 80))
        self.VehiclePlateNumberImage.setStyleSheet("border: 1px solid light blue;")
        self.VehiclePlateNumberImage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.VehiclePlateNumberImage.setText("")
        self.VehiclePlateNumberImage.setObjectName("VehiclePlateNumberImage")
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(36)
        self.VehiclePlateNumberTextImage = QtWidgets.QTextEdit(self.centralwidget)
        self.VehiclePlateNumberTextImage.setGeometry(QtCore.QRect(1130, 764, 282, 80))
        self.VehiclePlateNumberTextImage.setFont(font)
        self.VehiclePlateNumberTextImage.setStyleSheet("")
        self.VehiclePlateNumberTextImage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.VehiclePlateNumberTextImage.setText("")
        self.VehiclePlateNumberTextImage.setAlignment(QtCore.Qt.AlignLeft)
        self.VehiclePlateNumberTextImage.setObjectName("VehiclePlateNumberTextImage")
        self.VehiclePlateNumberTextImage.setReadOnly(True)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(50)
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(460, 546, 560, 32))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Browse = QtWidgets.QPushButton(self.layoutWidget)
        self.Browse.setFont(font)
        self.Browse.setStyleSheet("")
        self.Browse.setObjectName("Browse")
        self.horizontalLayout.addWidget(self.Browse)
        self.KNNBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.KNNBtn.setFont(font)
        self.KNNBtn.setStyleSheet("")
        self.KNNBtn.setObjectName("Detect")
        self.horizontalLayout.addWidget(self.KNNBtn)
        self.OCRBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.OCRBtn.setFont(font)
        self.OCRBtn.setStyleSheet("")
        self.OCRBtn.setObjectName("OCRBtn")
        self.horizontalLayout.addWidget(self.OCRBtn)
        self.CheckCarStatus = QtWidgets.QPushButton(self.layoutWidget)
        self.CheckCarStatus.setFont(font)
        self.CheckCarStatus.setStyleSheet("")
        self.CheckCarStatus.setObjectName("CheckCarStatus")
        self.horizontalLayout.addWidget(self.CheckCarStatus)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(1378, 194, 66, 128))
        self.widget.setObjectName("widget")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/adduser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RegisterBtn = QtWidgets.QPushButton(self.centralwidget)
        self.RegisterBtn.setGeometry(QtCore.QRect(1530, 182, 82, 60))
        self.RegisterBtn.setStyleSheet("")
        self.RegisterBtn.setText("")
        self.RegisterBtn.setIcon(icon1)
        self.RegisterBtn.setIconSize(QtCore.QSize(50, 50))
        self.RegisterBtn.setFlat(True)
        self.RegisterBtn.setObjectName("RegisterBtn")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/combochart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AnalysisBtn = QtWidgets.QPushButton(self.centralwidget)
        self.AnalysisBtn.setGeometry(QtCore.QRect(1530, 252, 82, 60))
        self.AnalysisBtn.setStyleSheet("")
        self.AnalysisBtn.setText("")
        self.AnalysisBtn.setIcon(icon2)
        self.AnalysisBtn.setIconSize(QtCore.QSize(50, 50))
        self.AnalysisBtn.setFlat(True)
        self.AnalysisBtn.setObjectName("Analysis")
        self.SignIn = QtWidgets.QPushButton(self.centralwidget)
        self.SignIn.setGeometry(QtCore.QRect(1305, 546, 50, 28))
        self.SignIn.setFont(font)
        self.SignIn.setStyleSheet("")
        self.SignIn.setObjectName("Sign In")
        self.SignOut = QtWidgets.QPushButton(self.centralwidget)
        self.SignOut.setGeometry(QtCore.QRect(1400, 546, 50, 28))
        self.SignOut.setFont(font)
        self.SignOut.setStyleSheet("")
        self.SignOut.setObjectName("Sign Out")
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionDesignHelp = QtWidgets.QAction(MainWindow)
        self.actionDesignHelp.setObjectName("actionDesignHelp")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAboutQt = QtWidgets.QAction(MainWindow)
        self.actionAboutQt.setObjectName("actionAboutQt")
        self.menuHelp.addAction(self.actionDesignHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAboutQt)
        self.menuBar.addAction(self.menuHelp.menuAction())
        # .raise_() = bring to front, .lower_() = send to back
        self.VVIPLabel.raise_()
        self.SpecialNeedLabel.raise_()
        self.ZoneALabel.raise_()
        self.VisitorsLabel.raise_()
        self.ZoneBLabel.raise_()
        self.layoutWidget.raise_()
        self.SiteCombox.raise_()
        self.Options.raise_()
        self.SiteLabel.raise_()
        self.clock.raise_()
        self.icon.raise_()
        self.RegistrationLabel.raise_()
        self.UploadedDataImage.raise_()
        self.SPSlabel.raise_()
        self.UploadedDataLabel.raise_()
        self.CarImage.raise_()
        self.ParkingNavigation.raise_()
        self.ZoneBbar.raise_()
        self.VVIParrow.raise_()
        self.VVIPText.raise_()
        self.VVIPSpaceLeft.raise_()
        self.VisitorsSpaceLeft.raise_()
        self.SpecialNeedbar.raise_()
        self.Visitorsbar.raise_()
        self.SpecialNeedText.raise_()
        self.ZoneBSpaceLeft.raise_()
        self.VVIPPercentageOccupied.raise_()
        self.ZoneAPercentageOccupied.raise_()
        self.ZoneBPercentageOccupied.raise_()
        self.SpecialNeedPercentageOccupied.raise_()
        self.VisitorsText.raise_()
        self.VVIPbar.raise_()
        self.VisitorsPercentageOccupied.raise_()
        self.ZoneText.raise_()
        self.ZoneAText.raise_()
        self.ZoneASpaceLeft.raise_()
        self.SpecialNeedSpaceLeft.raise_()
        self.ZoneAbar.raise_()
        self.VVIPOpenIcon.raise_()
        self.SpecialNeedOpenIcon.raise_()
        self.ZoneAOpenIcon.raise_()
        self.ZoneBOpenIcon.raise_()
        self.VisitorsOpenIcon.raise_()
        self.SpecialNeedarrow.raise_()
        self.ZoneAarrow.raise_()
        self.ZoneBarrow.raise_()
        self.Visitorsarrow.raise_()
        self.VehiclePlateNumberImage.raise_()
        self.StatusText.raise_()
        self.Status.raise_()
        self.VehiclePlateText.raise_()
        self.RegisterBtn.raise_()
        self.VehiclePlateNumberTextImage.raise_()
        self.VehiclePlateTextImage.raise_()
        self.plainTextEdit.raise_()
        self.AnalysisBtn.raise_()
        self.SignIn.raise_()
        self.SignOut.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.ParkingNavigation.addItem("Overview")
        self.Options.addItem("VVIP")
        self.Options.addItem("Special Need")
        self.Options.addItem("Zone A")
        self.Options.addItem("Zone B")
        self.Options.addItem("Visitors")
        self.ParkingNavigation.activated.connect(self.parking_navigation)
        self.Options.activated[str].connect(self.sign_in_out)
        self.AnalysisBtn.clicked.connect(self.parking_navigation_button)

        self.Browse.clicked.connect(self.browse)
        self.KNNBtn.clicked.connect(self.KNN)
        self.RegisterBtn.clicked.connect(self.register)
        self.OCRBtn.clicked.connect(self.sign_up_database)
        self.actionNew.triggered.connect(self.browse)
        self.actionDesignHelp.triggered.connect(contact_me)
        self.actionAbout.triggered.connect(about)
        self.actionAboutQt.triggered.connect(aboutQt)

        self.VVIP_percentage_current_sign_in = 0
        self.VVIP_spaceleft_current_sign_in = 100
        self.SpecialNeed_percentage_current_sign_in = 0
        self.SpecialNeed_spaceleft_current_sign_in = 100
        self.ZoneA_percentage_current_sign_in = 0
        self.ZoneA_spaceleft_current_sign_in = 100
        self.ZoneB_percentage_current_sign_in = 0
        self.ZoneB_spaceleft_current_sign_in = 100
        self.Visitors_percentage_current_sign_in = 0
        self.Visitors_spaceleft_current_sign_in = 100

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "app"))
        self.SiteCombox.setItemText(0, _translate("MainWindow", "New Item"))
        self.SiteCombox.setStatusTip(_translate("MainWindow", "Site Combo"))
        self.Options.setItemText(0, _translate("MainWindow", "---Select---"))
        self.Options.setStatusTip(_translate("MainWindow", "Options"))
        self.SiteLabel.setText(_translate("MainWindow", "Site"))
        self.SiteLabel.setStatusTip(_translate("MainWindow", "Site Label"))
        self.clock.setStatusTip(_translate("MainWindow", "Clock"))
        self.RegistrationLabel.setText(_translate("MainWindow", ""))
        self.RegistrationLabel.setStatusTip(_translate("MainWindow", "Registration Label"))
        self.SPSlabel.setText(_translate("MainWindow", ""))
        self.SPSlabel.setStatusTip(_translate("MainWindow", "SPS Label"))
        self.UploadedDataLabel.setText(_translate("MainWindow", "Upload data(Excel, CSV & Text)"))
        self.UploadedDataLabel.setStatusTip(_translate("MainWindow", "Uploaded Data Label"))
        self.ParkingNavigation.setItemText(0, _translate("MainWindow", "Parking"))
        self.ParkingNavigation.setStatusTip(_translate("MainWindow", "Parking Navigation"))
        self.VVIPText.setText(_translate("MainWindow", "VVIP Space"))
        self.VVIPText.setStatusTip(_translate("MainWindow", "VVIP"))
        self.VVIPSpaceLeft.setText(_translate("MainWindow", "100 free"))
        self.VVIPSpaceLeft.setStatusTip(_translate("MainWindow", "VVIP Space Left"))
        self.VisitorsSpaceLeft.setText(_translate("MainWindow", "100 free"))
        self.VisitorsSpaceLeft.setStatusTip(_translate("MainWindow", "Visitors Space Left"))
        self.SpecialNeedText.setText(_translate("MainWindow", "Special Need"))
        self.SpecialNeedText.setStatusTip(_translate("MainWindow", "Special Need"))
        self.ZoneBSpaceLeft.setText(_translate("MainWindow", "100 free"))
        self.ZoneBSpaceLeft.setStatusTip(_translate("MainWindow", "Zone B Space Left"))
        self.VVIPPercentageOccupied.setText(_translate("MainWindow", "0% occupied"))
        self.VVIPPercentageOccupied.setStatusTip(_translate("MainWindow", "VVIP Percentage Occupied"))
        self.ZoneAPercentageOccupied.setText(_translate("MainWindow", "0% occupied"))
        self.ZoneAPercentageOccupied.setStatusTip(_translate("MainWindow", "Zone A Percentage Occupied"))
        self.ZoneBPercentageOccupied.setText(_translate("MainWindow", "0% occupied"))
        self.ZoneBPercentageOccupied.setStatusTip(_translate("MainWindow", "Zone B Percentage Occupied"))
        self.SpecialNeedPercentageOccupied.setText(_translate("MainWindow", "0% occupied"))
        self.SpecialNeedPercentageOccupied.setStatusTip(_translate("MainWindow", "Special Need Percentage Occupied"))
        self.VisitorsText.setText(_translate("MainWindow", "Visitors"))
        self.VisitorsText.setStatusTip(_translate("MainWindow", "Visitors"))
        self.VisitorsPercentageOccupied.setText(_translate("MainWindow", "0% occupied"))
        self.VisitorsPercentageOccupied.setStatusTip(_translate("MainWindow", "Visitors Percentage Occupied"))
        self.ZoneText.setText(_translate("MainWindow", "Zone B"))
        self.ZoneText.setStatusTip(_translate("MainWindow", "Zone B"))
        self.ZoneAText.setText(_translate("MainWindow", "Zone A"))
        self.ZoneAText.setStatusTip(_translate("MainWindow", "Zone A"))
        self.ZoneASpaceLeft.setText(_translate("MainWindow", "100 free"))
        self.ZoneASpaceLeft.setStatusTip(_translate("MainWindow", "Zone A Space Left"))
        self.SpecialNeedSpaceLeft.setText(_translate("MainWindow", "100 free"))
        self.SpecialNeedSpaceLeft.setStatusTip(_translate("MainWindow", "Special Need Space Left"))
        self.StatusText.setText(_translate("MainWindow", "Status:"))
        self.StatusText.setStatusTip(_translate("MainWindow", "Status"))
        self.VehiclePlateText.setText(_translate("MainWindow", "Vehicle Plate:"))
        self.VehiclePlateText.setStatusTip(_translate("MainWindow", "Vehicle Plate"))
        self.VehiclePlateTextImage.setText(_translate("MainWindow", "Vehicle Plate Number:"))
        self.VehiclePlateTextImage.setStatusTip(_translate("MainWindow", "Vehicle Plate Number"))
        self.Browse.setText(_translate("MainWindow", "Browse"))
        self.Browse.setStatusTip(_translate("MainWindow", "Browse"))
        self.KNNBtn.setText(_translate("MainWindow", "KNN"))
        self.KNNBtn.setStatusTip(_translate("MainWindow", "KNN classification"))
        self.CheckCarStatus.setText(_translate("MainWindow", "Check Status"))
        self.CheckCarStatus.setStatusTip(_translate("MainWindow", "Check Status"))
        self.OCRBtn.setText(_translate("MainWindow", "OCR"))
        self.OCRBtn.setStatusTip(_translate("MainWindow", "OCR"))
        self.RegisterBtn.setStatusTip(_translate("MainWindow", "Register icon"))
        self.AnalysisBtn.setStatusTip(_translate("MainWindow", "Analysis icon"))
        self.SignIn.setText(_translate("MainWindow", "Sign in"))
        self.SignIn.setStatusTip(_translate("MainWindow", "Sign in"))
        self.SignOut.setText(_translate("MainWindow", "Sign out"))
        self.SignOut.setStatusTip(_translate("MainWindow", "Sign out"))
        self.icon.setStatusTip(_translate("MainWindow", "Icon"))
        self.VehiclePlateNumberImage.setStatusTip(_translate("MainWindow", "Cropped Image"))
        self.plainTextEdit.setStatusTip(_translate("MainWindow", "Note"))
        self.VVIPbar.setStatusTip(_translate("MainWindow", "VVIP bar"))
        self.SpecialNeedbar.setStatusTip(_translate("MainWindow", "Special Need bar"))
        self.ZoneAbar.setStatusTip(_translate("MainWindow", "Zone A bar"))
        self.ZoneBbar.setStatusTip(_translate("MainWindow", "Zone B bar"))
        self.Visitorsbar.setStatusTip(_translate("MainWindow", "Visitors bar"))
        self.VehiclePlateNumberTextImage.setStatusTip(_translate("MainWindow", "License plate number"))
        self.UploadedDataImage.setStatusTip(_translate("MainWindow", "Parking lot"))
        self.CarImage.setStatusTip(_translate("MainWindow", "Import Image"))
        self.Status.setStatusTip(_translate("MainWindow", "Vehicle status"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionNew.setStatusTip(_translate("MainWindow", "Browse"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionDesignHelp.setText(_translate("MainWindow", "Designer Help"))
        self.actionDesignHelp.setShortcut(_translate("MainWindow", "Ctrl+?"))
        self.actionDesignHelp.setStatusTip(_translate("MainWindow", "Need help?"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setStatusTip(_translate("MainWindow", "About project"))
        self.actionAboutQt.setText(_translate("MainWindow", "About Qt"))
        self.actionAboutQt.setStatusTip(_translate("MainWindow", "About Qt"))

    def browse(self):
        file_path = QFileDialog.getOpenFileName(self.window, 'Open file',
                                                '', "Image files (*.jpg *.png *.jpeg)")
        self.image = file_path
        img = file_path[0]
        pyperclip.copy(file_path[0])
        pixmap = QPixmap(img)
        pixmapResize = pixmap.scaled(660, 420)
        self.CarImage.setPixmap(pixmapResize)

    def KNN(self):
        self.panel = product2.start()
        CarImage = QtGui.QPixmap("./imgOriginalScene.png")
        CarImageResize = CarImage.scaled(660, 420)
        self.CarImage.setPixmap(CarImageResize)
        self.CheckCarStatus.clicked.connect(self.KNN_status)

    def ocr(self):
        def decode_predictions(scores, geometry):
            # grab the number of rows and columns from the scores volume, then
            # initialize our set of bounding box rectangles and corresponding
            # confidence scores
            (numRows, numCols) = scores.shape[2:4]
            rects = []
            confidences = []

            # loop over the number of rows
            for y in range(0, numRows):
                # extract the scores (probabilities), followed by the
                # geometrical data used to derive potential bounding box
                # coordinates that surround text
                scoresData = scores[0, 0, y]
                xData0 = geometry[0, 0, y]
                xData1 = geometry[0, 1, y]
                xData2 = geometry[0, 2, y]
                xData3 = geometry[0, 3, y]
                anglesData = geometry[0, 4, y]

                # loop over the number of columns
                for x in range(0, numCols):
                    # if our score does not have sufficient probability,
                    # ignore it
                    if scoresData[x] < args["min_confidence"]:
                        continue

                    # compute the offset factor as our resulting feature
                    # maps will be 4x smaller than the input image
                    (offsetX, offsetY) = (x * 4.0, y * 4.0)

                    # extract the rotation angle for the prediction and
                    # then compute the sin and cosine
                    angle = anglesData[x]
                    cos = np.cos(angle)
                    sin = np.sin(angle)

                    # use the geometry volume to derive the width and height
                    # of the bounding box
                    h = xData0[x] + xData2[x]
                    w = xData1[x] + xData3[x]

                    # compute both the starting and ending (x, y)-coordinates
                    # for the text prediction bounding box
                    endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                    endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                    startX = int(endX - w)
                    startY = int(endY - h)

                    # add the bounding box coordinates and probability score
                    # to our respective lists
                    rects.append((startX, startY, endX, endY))
                    confidences.append(scoresData[x])

            # return a tuple of the bounding boxes and associated confidences
            return (rects, confidences)

        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", type=str,
                        help="path to input image")
        ap.add_argument("-east", "--east", type=str,
                        help="path to input EAST text detector")
        ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
                        help="minimum probability required to inspect a region")
        ap.add_argument("-w", "--width", type=int, default=320,
                        help="nearest multiple of 32 for resized width")
        ap.add_argument("-e", "--height", type=int, default=320,
                        help="nearest multiple of 32 for resized height")
        ap.add_argument("-p", "--padding", type=float, default=0.0,
                        help="amount of padding to add to each border of ROI")
        args = vars(ap.parse_args())

        # load the input image and grab the image dimensions
        image = cv2.imread(pyperclip.paste())
        orig = image.copy()
        (origH, origW) = image.shape[:2]

        # set the new width and height and then determine the ratio in change
        # for both the width and height
        (newW, newH) = (args["width"], args["height"])
        rW = origW / float(newW)
        rH = origH / float(newH)

        # resize the image and grab the new image dimensions
        image = cv2.resize(image, (newW, newH))
        (H, W) = image.shape[:2]

        # define the two output layer names for the EAST detector model that
        # we are interested in -- the first is the output probabilities and the
        # second can be used to derive the bounding box coordinates of text
        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"]

        # load the pre-trained EAST text detector
        print("[INFO] loading EAST text detector...")
        net = cv2.dnn.readNet("frozen_east_text_detection.pb")

        # construct a blob from the image and then perform a forward pass of
        # the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                     (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)

        # decode the predictions, then  apply non-maxima suppression to
        # suppress weak, overlapping bounding boxes
        (rects, confidences) = decode_predictions(scores, geometry)
        boxes = non_max_suppression(np.array(rects), probs=confidences)

        # initialize the list of results
        results = []

        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)

            # in order to obtain a better OCR of the text we can potentially
            # apply a bit of padding surrounding the bounding box -- here we
            # are computing the deltas in both the x and y directions
            dX = int((endX - startX) * args["padding"])
            dY = int((endY - startY) * args["padding"])

            # apply padding to each side of the bounding box, respectively
            startX = max(0, startX - dX)
            startY = max(0, startY - dY)
            endX = min(origW, endX + (dX * 2))
            endY = min(origH, endY + (dY * 2))

            # extract the actual padded ROI
            roi = orig[startY:endY, startX:endX]

            # in order to apply Tesseract v4 to OCR text we must supply
            # (1) a language, (2) an OEM flag of 4, indicating that the we
            # wish to use the LSTM neural net model for OCR, and finally
            # (3) an OEM value, in this case, 7 which implies that we are
            # treating the ROI as a single line of text
            config = ("-l eng --oem 1 --psm 7")
            text = pytesseract.image_to_string(roi, config=config)

            # add the bounding box coordinates and OCR'd text to the list
            # of results
            results.append(((startX, startY, endX, endY), text))

        # sort the results bounding box coordinates from top to bottom
        results = sorted(results, key=lambda r: r[0][1])

        # loop over the results
        for ((startX, startY, endX, endY), text) in results:
            # display the text OCR'd by Tesseract
            with open('./txt/ocr_vehicle_plate_number.txt', 'w') as f:
                print("{}".format(text), file=f)

            # strip out non-ASCII text so we can draw the text on the image
            # using OpenCV, then draw the text and a bounding box surrounding
            # the text region of the input image
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            output = orig.copy()
            cv2.rectangle(output, (startX, startY), (endX, endY),
                          (0, 0, 255), 2)
            cv2.putText(output, text, (startX, startY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            image_crop = output[startY:endY, startX:endX]

            # show the output image
            cv2.imwrite("./detection/crop_image.jpg", image_crop)
            cv2.imwrite("result.jpg", output)
            CarImage = QtGui.QPixmap("./result.jpg")
            CarImageResize = CarImage.scaled(660, 420)
            self.CarImage.setPixmap(CarImageResize)
            self.CheckCarStatus.clicked.connect(self.ocr_status)
            cv2.waitKey(0)

        return text

    def KNN_status(self):
        text = open('./txt/knn_vehicle_details.txt').read()
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Status.setFont(font)
        self.Status.setText(text)
        plate_image = QtGui.QPixmap("./imgPlate.png")
        plate_image_resized = plate_image.scaled(282, 80)
        self.VehiclePlateNumberImage.setPixmap(plate_image_resized)

        text2 = open("./txt/knn_vehicle_plate_number.txt").read()
        font2 = QtGui.QFont()
        font2.setFamily("Consolas")
        font2.setPointSize(34)
        font2.setBold(True)
        font2.setWeight(75)
        self.VehiclePlateNumberTextImage.setFont(font2)
        self.VehiclePlateNumberTextImage.setText(text2)

    def ocr_status(self):
        text = open('./txt/ocr_vehicle_details.txt').read()
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Status.setFont(font)
        self.Status.setText(text)
        plate_image = QtGui.QPixmap("./detection/crop_image.jpg")
        plate_image_resized = plate_image.scaled(282, 80)
        self.VehiclePlateNumberImage.setPixmap(plate_image_resized)

        text2 = open("./txt/ocr_vehicle_plate_number.txt").read()
        font2 = QtGui.QFont()
        font2.setFamily("Consolas")
        font2.setPointSize(34)
        font2.setBold(True)
        font2.setWeight(75)
        self.VehiclePlateNumberTextImage.setFont(font2)
        self.VehiclePlateNumberTextImage.setText(text2)

    def sign_up_database(self):
        conn = mysql.connector.connect(host='localhost', user='root', port=3306, password='',
                                       db='register', auth_plugin='mysql_native_password')
        c1 = conn.cursor()
        license_plate = self.ocr()
        c1.execute('SELECT * FROM sps_data where vehicle_plate_number=%s', (license_plate,))
        r = c1.fetchone()
        if r is not None:
            with open('./txt/ocr_vehicle_details.txt', 'w') as f:
                print("Details:", file=f)
                print("ID : " + r[0], file=f)
                print("F_NO : " + r[1], file=f)
                # print("Employee ID : " + r[2], file=f)
                # print("Employee Name : " + r[3], file=f)
                print("Department : " + r[4], file=f)
                # print("Role : " + r[6], file=f)
                # print("Shift pattern : " + r[6], file=f)
                # print("Mobile Number : " + r[7], file=f)
                # print("Request date : " + r[8], file=f)
                # print("Request type : " + r[9], file=f)
                print("Vehicle type : " + r[10], file=f)
                print("Vehicle model : " + r[11], file=f)
                print("Vehicle plate number : " + r[12], file=f)
                print("Vehicle color : " + r[13], file=f)
                print("Area : " + r[16], file=f)
                print("======================================", file=f)
                print("Authorized vehicle", file=f)

        else:
            with open('./txt/ocr_vehicle_details.txt', 'w') as f:
                print("Unauthorized vehicle", file=f)

    def register(self):
        self.signup = QtWidgets.QMainWindow()
        self.ui = Ui_signup()
        self.ui.setupUi(self.signup)
        self.signup.show()

    def parking_navigation(self):
        if self.ParkingNavigation.currentIndex() == 1:
            self.Overview = QtWidgets.QMainWindow()
            self.ui = Ui_Overview()
            self.ui.overviewUi(self.Overview)
            self.Overview.show()

    def parking_navigation_button(self):
        self.Overview = QtWidgets.QMainWindow()
        self.ui = Ui_Overview()
        self.ui.overviewUi(self.Overview)
        self.Overview.show()

    def sign_in_out(self, text):
        if text == "VVIP":
            self.SignIn.clicked.connect(self.VVIP_sign_in)
            self.SignOut.clicked.connect(self.VVIP_sign_out)
            self.VVIP_running = True

        elif text == "Special Need":
            self.SignIn.clicked.connect(self.Special_sign_in)
            self.SignOut.clicked.connect(self.Special_sign_out)
            self.SpecialNeed_running = True


        elif text == "Zone A":
            self.SignIn.clicked.connect(self.ZoneA_sign_in)
            self.SignOut.clicked.connect(self.ZoneA_sign_out)
            self.ZoneA_running = True

        elif text == "Zone B":
            self.SignIn.clicked.connect(self.ZoneB_sign_in)
            self.SignOut.clicked.connect(self.ZoneB_sign_out)
            self.ZoneB_running = True


        elif text == "Visitors":
            self.SignIn.clicked.connect(self.Visitors_sign_in)
            self.SignOut.clicked.connect(self.Visitors_sign_out)
            self.Visitors_running = True

    def sign_in_out_db(self):
        con = pymysql.connect(host='localhost', user='root', port=3306, password='',
                              db='register')
        cur = con.cursor()
        unix = int(time.time())
        text = open("./txt/ocr_vehicle_plate_number.txt").read()
        # hour = str(datetime.datetime.fromtimestamp(unix).strftime('%H'))
        timestamp = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        area = self.Options.currentText()
        cur.execute(
            "INSERT INTO sign_in_out(vehicle_plate_number, timestamp, status, area) "
            "VALUES('%s', '%s', '%s', '%s')" % (text, timestamp, self.status, area))
        con.commit()
        show_inserted_popup()

    def VVIP_sign_in(self):
        if self.VVIP_running:
            self.status = self.SignIn.text()
            self.sign_in_out_db()
            self.VVIP_percentage_current_sign_in += 1
            self.VVIPPercentageOccupied.setText(str(self.VVIP_percentage_current_sign_in) + "% Occupied")
            self.VVIP_spaceleft_current_sign_in -= 1
            self.VVIPSpaceLeft.setText(str(self.VVIP_spaceleft_current_sign_in) + " free")
            self.VVIPbar.setValue(self.VVIP_percentage_current_sign_in)
            self.VVIP_running = False
            if self.VVIP_percentage_current_sign_in >= 100:
                self.VVIPOpenIcon.setPixmap(QtGui.QPixmap("./icon/closed.png"))
                self.VVIPbar.setStyleSheet(open("./qss/100%.qss", "r").read())
                show_full_popup()

    def Special_sign_in(self):
        if self.SpecialNeed_running:
            self.status = self.SignIn.text()
            self.sign_in_out_db()
            self.SpecialNeed_percentage_current_sign_in += 1
            self.SpecialNeedPercentageOccupied.setText(
                str(self.SpecialNeed_percentage_current_sign_in) + "% Occupied")
            self.SpecialNeed_spaceleft_current_sign_in -= 1
            self.SpecialNeedSpaceLeft.setText(str(self.SpecialNeed_spaceleft_current_sign_in) + " free")
            self.SpecialNeedbar.setValue(self.SpecialNeed_percentage_current_sign_in)
            self.SpecialNeed_running = False
            if self.SpecialNeed_percentage_current_sign_in >= 100:
                self.SpecialNeedOpenIcon.setPixmap(QtGui.QPixmap("./icon/closed.png"))
                self.SpecialNeedbar.setStyleSheet(open("./qss/100%.qss", "r").read())
                show_full_popup()

    def ZoneA_sign_in(self):
        if self.ZoneA_running:
            self.status = self.SignIn.text()
            self.sign_in_out_db()
            self.ZoneA_percentage_current_sign_in += 1
            self.ZoneAPercentageOccupied.setText(str(self.ZoneA_percentage_current_sign_in) + "% Occupied")
            self.ZoneA_spaceleft_current_sign_in -= 1
            self.ZoneASpaceLeft.setText(str(self.ZoneA_spaceleft_current_sign_in) + " free")
            self.ZoneAbar.setValue(self.ZoneA_percentage_current_sign_in)
            self.ZoneA_running = False
            if self.ZoneA_percentage_current_sign_in >= 100:
                self.ZoneAOpenIcon.setPixmap(QtGui.QPixmap("./icon/closed.png"))
                self.ZoneAbar.setStyleSheet(open("./qss/100%.qss", "r").read())
                show_full_popup()

    def ZoneB_sign_in(self):
        if self.ZoneB_running:
            self.status = self.SignIn.text()
            self.sign_in_out_db()
            self.ZoneB_percentage_current_sign_in += 1
            self.ZoneBPercentageOccupied.setText(str(self.ZoneB_percentage_current_sign_in) + "% Occupied")
            self.ZoneB_spaceleft_current_sign_in -= 1
            self.ZoneBSpaceLeft.setText(str(self.ZoneB_spaceleft_current_sign_in) + " free")
            self.ZoneBbar.setValue(self.ZoneB_percentage_current_sign_in)
            self.ZoneB_running = False
            if self.ZoneB_percentage_current_sign_in >= 100:
                self.ZoneBOpenIcon.setPixmap(QtGui.QPixmap("./icon/closed.png"))
                self.ZoneBbar.setStyleSheet(open("./qss/100%.qss", "r").read())
                show_full_popup()

    def Visitors_sign_in(self):
        if self.Visitors_running:
            self.status = self.SignIn.text()
            self.sign_in_out_db()
            self.Visitors_percentage_current_sign_in += 1
            self.VisitorsPercentageOccupied.setText(str(self.Visitors_percentage_current_sign_in) + "% Occupied")
            self.Visitors_spaceleft_current_sign_in -= 1
            self.VisitorsSpaceLeft.setText(str(self.Visitors_spaceleft_current_sign_in) + " free")
            self.Visitorsbar.setValue(self.Visitors_percentage_current_sign_in)
            self.Visitors_running = False
            if self.Visitors_percentage_current_sign_in >= 100:
                self.VisitorsOpenIcon.setPixmap(QtGui.QPixmap("./icon/closed.png"))
                self.Visitorsbar.setStyleSheet(open("./qss/100%.qss", "r").read())
                show_full_popup()

    def VVIP_sign_out(self):
        if self.VVIP_running:
            self.status = self.SignOut.text()
            self.sign_in_out_db()
            self.VVIP_percentage_current_sign_in -= 1
            self.VVIPPercentageOccupied.setText(str(self.VVIP_percentage_current_sign_in) + "% Occupied")
            self.VVIP_spaceleft_current_sign_in += 1
            self.VVIPSpaceLeft.setText(str(self.VVIP_spaceleft_current_sign_in) + " free")
            self.VVIPbar.setValue(self.VVIP_percentage_current_sign_in)
            self.VVIP_running = False
            if self.VVIP_percentage_current_sign_in < 1:
                show_empty_popup()
            elif self.VVIP_percentage_current_sign_in <= 99:
                self.VVIPOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
                self.VVIPbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())

    def Special_sign_out(self):
        if self.SpecialNeed_running:
            self.status = self.SignOut.text()
            self.sign_in_out_db()
            self.SpecialNeed_percentage_current_sign_in -= 1
            self.SpecialNeedPercentageOccupied.setText(
                str(self.SpecialNeed_percentage_current_sign_in) + "% Occupied")
            self.SpecialNeed_spaceleft_current_sign_in += 1
            self.SpecialNeedSpaceLeft.setText(str(self.SpecialNeed_spaceleft_current_sign_in) + " free")
            self.SpecialNeedbar.setValue(self.SpecialNeed_percentage_current_sign_in)
            self.SpecialNeed_running = False
            if self.SpecialNeed_percentage_current_sign_in < 1:
                show_empty_popup()
            elif self.SpecialNeed_percentage_current_sign_in <= 99:
                self.SpecialNeedOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
                self.SpecialNeedbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())

    def ZoneA_sign_out(self):
        if self.ZoneA_running:
            self.status = self.SignOut.text()
            self.sign_in_out_db()
            self.ZoneA_percentage_current_sign_in -= 1
            self.ZoneAPercentageOccupied.setText(str(self.ZoneA_percentage_current_sign_in) + "% Occupied")
            self.ZoneA_spaceleft_current_sign_in += 1
            self.ZoneASpaceLeft.setText(str(self.ZoneA_spaceleft_current_sign_in) + " free")
            self.ZoneAbar.setValue(self.ZoneA_percentage_current_sign_in)
            self.ZoneA_running = False
            if self.ZoneA_percentage_current_sign_in < 1:
                show_empty_popup()
            elif self.ZoneA_percentage_current_sign_in <= 99:
                self.ZoneAOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
                self.ZoneAbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())

    def ZoneB_sign_out(self):
        if self.ZoneB_running:
            self.status = self.SignOut.text()
            self.sign_in_out_db()
            self.ZoneB_percentage_current_sign_in -= 1
            self.ZoneBPercentageOccupied.setText(str(self.ZoneB_percentage_current_sign_in) + "% Occupied")
            self.ZoneB_spaceleft_current_sign_in += 1
            self.ZoneBSpaceLeft.setText(str(self.ZoneB_spaceleft_current_sign_in) + " free")
            self.ZoneBbar.setValue(self.ZoneB_percentage_current_sign_in)
            self.ZoneB_running = False
            if self.ZoneB_percentage_current_sign_in < 1:
                show_empty_popup()
            elif self.ZoneB_percentage_current_sign_in <= 99:
                self.ZoneBOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
                self.ZoneBbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())

    def Visitors_sign_out(self):
        if self.Visitors_running:
            self.status = self.SignOut.text()
            self.sign_in_out_db()
            self.Visitors_percentage_current_sign_in -= 1
            self.VisitorsPercentageOccupied.setText(str(self.Visitors_percentage_current_sign_in) + "% Occupied")
            self.Visitors_spaceleft_current_sign_in += 1
            self.VisitorsSpaceLeft.setText(str(self.Visitors_spaceleft_current_sign_in) + " free")
            self.Visitorsbar.setValue(self.Visitors_percentage_current_sign_in)
            self.Visitors_running = False
            if self.Visitors_percentage_current_sign_in < 1:
                show_empty_popup()
            elif self.Visitors_percentage_current_sign_in <= 99:
                self.VisitorsOpenIcon.setPixmap(QtGui.QPixmap("./icon/open.png"))
                self.Visitorsbar.setStyleSheet(open("./qss/0_to_99%.qss", "r").read())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainApp = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainApp)
    MainApp.show()
    sys.exit(app.exec_())
