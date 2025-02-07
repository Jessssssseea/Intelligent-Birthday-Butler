# -*- coding:utf-8 -*-
import sys
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget, QPushButton, QHeaderView, QAbstractItemView, QInputDialog,
    QMessageBox, QCalendarWidget, QRadioButton, QButtonGroup, QLabel, QGridLayout, QDialog
)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QIcon
import sxtwl


class BirthdayReminder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("生日提醒程序")
        self.setFixedSize(1000, 800)
        self.setWindowIcon(QIcon('files/cake.ico'))
        self.setStyleSheet(u"/*\n"
                           "Ubuntu Style Sheet for QT Applications\n"
                           "Author: Jaime A. Quiroga P.\n"
                           "Company: GTRONICK\n"
                           "Last updated: 01/10/2021 (dd/mm/yyyy), 15:18.\n"
                           "Available at: https://github.com/GTRONICK/QSS/blob/master/Ubuntu.qss\n"
                           "*/\n"
                           "QMainWindow {\n"
                           "	background-color:#f0f0f0;\n"
                           "}\n"
                           "QCheckBox {\n"
                           "	padding:2px;\n"
                           "}\n"
                           "QCheckBox:hover {\n"
                           "	border:1px solid rgb(255,150,60);\n"
                           "	border-radius:4px;\n"
                           "	padding: 1px;\n"
                           "	background-color:qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(190, 90, 50, 50), stop:1 rgba(250, 130, 40, 50));\n"
                           "}\n"
                           "QCheckBox::indicator:checked {\n"
                           "	border:1px solid rgb(246, 134, 86);\n"
                           "	border-radius:4px;\n"
                           "  	background-color:rgb(246, 134, 86)\n"
                           "}\n"
                           "QCheckBox::indicator:unchecked {\n"
                           "	border-width:1px solid rgb(246, 134, 86);\n"
                           "	border-radius:4px;\n"
                           "  	background-color:rgb(255,255,255);\n"
                           "}\n"
                           "QColorDialog {\n"
                           "	background-color:#f0f0f0;\n"
                           "}\n"
                           "QComboBox {\n"
                           "	color:rgb(81,72,65);\n"
                           "	background: #ffffff;\n"
                           "}\n"
                           "QComboBox:ed"
                           "itable {\n"
                           "	selection-color:rgb(81,72,65);\n"
                           "	selection-background-color: #ffffff;\n"
                           "}\n"
                           "QComboBox QAbstractItemView {\n"
                           "	selection-color: #ffffff;\n"
                           "	selection-background-color: rgb(246, 134, 86);\n"
                           "}\n"
                           "QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
                           "	color:  #1e1d23;	\n"
                           "}\n"
                           "QDateTimeEdit, QDateEdit, QDoubleSpinBox, QFontComboBox {\n"
                           "	color:rgb(81,72,65);\n"
                           "	background-color: #ffffff;\n"
                           "}\n"
                           "\n"
                           "QDialog {\n"
                           "	background-color:#f0f0f0;\n"
                           "}\n"
                           "\n"
                           "QLabel,QLineEdit {\n"
                           "	color:rgb(17,17,17);\n"
                           "}\n"
                           "QLineEdit {\n"
                           "	background-color:rgb(255,255,255);\n"
                           "	selection-background-color:rgb(236,116,64);\n"
                           "}\n"
                           "QMenuBar {\n"
                           "	color:rgb(223,219,210);\n"
                           "	background-color:rgb(65,64,59);\n"
                           "}\n"
                           "QMenuBar::item {\n"
                           "	padding-top:4px;\n"
                           "	padding-left:4px;\n"
                           "	padding-right:4px;\n"
                           "	color:rgb(223,219,210);\n"
                           "	background-color:rgb(65,64,59);\n"
                           "}\n"
                           "QMenuBar::item:selected {\n"
                           "	color:rgb(255,255,255);\n"
                           "	padding-top:2px;\n"
                           "	padding-left:2px;\n"
                           "	paddin"
                           "g-right:2px;\n"
                           "	border-top-width:2px;\n"
                           "	border-left-width:2px;\n"
                           "	border-right-width:2px;\n"
                           "	border-top-right-radius:4px;\n"
                           "	border-top-left-radius:4px;\n"
                           "	border-style:solid;\n"
                           "	background-color:rgb(65,64,59);\n"
                           "	border-top-color: rgb(47,47,44);\n"
                           "	border-right-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(90, 87, 78, 255), stop:1 rgba(47,47,44, 255));\n"
                           "	border-left-color:  qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(90, 87, 78, 255), stop:1 rgba(47,47,44, 255));\n"
                           "}\n"
                           "QMenu {\n"
                           "	color:rgb(223,219,210);\n"
                           "	background-color:rgb(65,64,59);\n"
                           "}\n"
                           "QMenu::item {\n"
                           "	color:rgb(223,219,210);\n"
                           "	padding:4px 10px 4px 20px;\n"
                           "}\n"
                           "QMenu::item:selected {\n"
                           "	color:rgb(255,255,255);\n"
                           "	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(225, 108, 54, 255), stop:1 rgba(246, 134, 86, 255));\n"
                           "	border-style:solid;\n"
                           "	border-width:3px;\n"
                           "	padding:4px 7px 4px 17px;\n"
                           "	border-bottom-color:qlineargra"
                           "dient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(175,85,48,255), stop:1 rgba(236,114,67, 255));\n"
                           "	border-top-color:qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));\n"
                           "	border-right-color:qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));\n"
                           "	border-left-color:qlineargradient(spread:pad, x1:1, y1:0.5, x2:0, y2:0.5, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));\n"
                           "}\n"
                           "QPlainTextEdit {\n"
                           "	border: 1px solid transparent;\n"
                           "	color:rgb(17,17,17);\n"
                           "	selection-background-color:rgb(236,116,64);\n"
                           "    background-color: #FFFFFF;\n"
                           "}\n"
                           "QProgressBar {\n"
                           "	text-align: center;\n"
                           "	color: rgb(0, 0, 0);\n"
                           "	border: 1px inset rgb(150,150,150); \n"
                           "	border-radius: 10px;\n"
                           "	background-color:rgb(221,221,219);\n"
                           "}\n"
                           "QProgressBar::chunk:horizontal {\n"
                           "	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(225, 108, 54"
                           ", 255), stop:1 rgba(246, 134, 86, 255));\n"
                           "	border:1px solid;\n"
                           "	border-radius:8px;\n"
                           "	border-bottom-color:qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(175,85,48,255), stop:1 rgba(236,114,67, 255));\n"
                           "	border-top-color:qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));\n"
                           "	border-right-color:qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));\n"
                           "	border-left-color:qlineargradient(spread:pad, x1:1, y1:0.5, x2:0, y2:0.5, stop:0 rgba(253,156,113,255), stop:1 rgba(205,90,46, 255));\n"
                           "}\n"
                           "QPushButton{\n"
                           "	color:rgb(17,17,17);\n"
                           "	border-width: 1px;\n"
                           "	border-radius: 6px;\n"
                           "	border-bottom-color: rgb(150,150,150);\n"
                           "	border-right-color: rgb(165,165,165);\n"
                           "	border-left-color: rgb(165,165,165);\n"
                           "	border-top-color: rgb(180,180,180);\n"
                           "	border-style: solid;\n"
                           "	padding: 13px;\n"
                           "	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2"
                           ":0.5, y2:0, stop:0 rgba(220, 220, 220, 255), stop:1 rgba(255, 255, 255, 255));\n"
                           "}\n"
                           "QPushButton:hover{\n"
                           "	color:rgb(17,17,17);\n"
                           "	border-width: 1px;\n"
                           "	border-radius:6px;\n"
                           "	border-top-color: rgb(255,150,60);\n"
                           "	border-right-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 255));\n"
                           "	border-left-color:  qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 255));\n"
                           "	border-bottom-color: rgb(200,70,20);\n"
                           "	border-style: solid;\n"
                           "	padding: 2px;\n"
                           "	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(220, 220, 220, 255), stop:1 rgba(255, 255, 255, 255));\n"
                           "}\n"
                           "QPushButton:default{\n"
                           "	color:rgb(17,17,17);\n"
                           "	border-width: 1px;\n"
                           "	border-radius:6px;\n"
                           "	border-top-color: rgb(255,150,60);\n"
                           "	border-right-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 255));\n"
                           "	bor"
                           "der-left-color:  qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 255));\n"
                           "	border-bottom-color: rgb(200,70,20);\n"
                           "	border-style: solid;\n"
                           "	padding: 2px;\n"
                           "	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(220, 220, 220, 255), stop:1 rgba(255, 255, 255, 255));\n"
                           "}\n"
                           "QPushButton:pressed{\n"
                           "	color:rgb(17,17,17);\n"
                           "	border-width: 1px;\n"
                           "	border-radius: 6px;\n"
                           "	border-width: 1px;\n"
                           "	border-top-color: rgba(255,150,60,200);\n"
                           "	border-right-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 200));\n"
                           "	border-left-color:  qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(200, 70, 20, 255), stop:1 rgba(255,150,60, 200));\n"
                           "	border-bottom-color: rgba(200,70,20,200);\n"
                           "	border-style: solid;\n"
                           "	padding: 2px;\n"
                           "	background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(220, 220, 220, 255), stop"
                           ":1 rgba(255, 255, 255, 255));\n"
                           "}\n"
                           "QPushButton:disabled{\n"
                           "	color:rgb(174,167,159);\n"
                           "	border-width: 1px;\n"
                           "	border-radius: 6px;\n"
                           "	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(200, 200, 200, 255), stop:1 rgba(230, 230, 230, 255));\n"
                           "}\n"
                           "QRadioButton {\n"
                           "	padding: 2px;\n"
                           "}\n"
                           "QRadioButton::indicator:checked {\n"
                           "	height: 10px;\n"
                           "	width: 10px;\n"
                           "	border-style:solid;\n"
                           "	border-radius:5px;\n"
                           "	border-width: 1px;\n"
                           "	border-color: rgba(246, 134, 86, 255);\n"
                           "	color: #a9b7c6;\n"
                           "	background-color:rgba(246, 134, 86, 255);\n"
                           "}\n"
                           "QRadioButton::indicator:!checked {\n"
                           "	height: 10px;\n"
                           "	width: 10px;\n"
                           "	border-style:solid;\n"
                           "	border-radius:5px;\n"
                           "	border-width: 1px;\n"
                           "	border-color: rgb(246, 134, 86);\n"
                           "	color: #a9b7c6;\n"
                           "	background-color: transparent;\n"
                           "}\n"
                           "QScrollArea {\n"
                           "	color: white;\n"
                           "	background-color:#f0f0f0;\n"
                           "}\n"
                           "QSlider::groove {\n"
                           "	border-style: solid;\n"
                           "	border-width: 1px;\n"
                           "	border-color: rgb(207,"
                           "207,207);\n"
                           "}\n"
                           "QSlider::groove:horizontal {\n"
                           "	height: 5px;\n"
                           "	background: rgb(246, 134, 86);\n"
                           "}\n"
                           "QSlider::groove:vertical {\n"
                           "	width: 5px;\n"
                           "	background: rgb(246, 134, 86);\n"
                           "}\n"
                           "QSlider::handle:horizontal {\n"
                           "	background: rgb(253,253,253);\n"
                           "	border-style: solid;\n"
                           "	border-width: 1px;\n"
                           "	border-color: rgb(207,207,207);\n"
                           "	width: 12px;\n"
                           "	margin: -5px 0;\n"
                           "	border-radius: 7px;\n"
                           "}\n"
                           "QSlider::handle:vertical {\n"
                           "	background: rgb(253,253,253);\n"
                           "	border-style: solid;\n"
                           "	border-width: 1px;\n"
                           "	border-color: rgb(207,207,207);\n"
                           "	height: 12px;\n"
                           "	margin: 0 -5px;\n"
                           "	border-radius: 7px;\n"
                           "}\n"
                           "QSlider::add-page:horizontal, QSlider::add-page:vertical {\n"
                           " 	background: white;\n"
                           "}\n"
                           "QSlider::sub-page:horizontal, QSlider::sub-page:vertical {\n"
                           "	background: rgb(246, 134, 86);\n"
                           "}\n"
                           "QStatusBar, QSpinBox {\n"
                           "	color:rgb(81,72,65);\n"
                           "}\n"
                           "QSpinBox {\n"
                           "	background-color: #ffffff;\n"
                           "}\n"
                           "QScrollBar:horizontal {\n"
                           "	max-height: 20px;\n"
                           "	border: 1p"
                           "x transparent;\n"
                           "	margin: 0px 20px 0px 20px;\n"
                           "}\n"
                           "QScrollBar::handle:horizontal {\n"
                           "	background: rgb(253,253,253);\n"
                           "	border: 1px solid rgb(207,207,207);\n"
                           "	border-radius: 7px;\n"
                           "	min-width: 25px;\n"
                           "}\n"
                           "QScrollBar::handle:horizontal:hover {\n"
                           "	background: rgb(253,253,253);\n"
                           "	border: 1px solid rgb(255,150,60);\n"
                           "	border-radius: 7px;\n"
                           "	min-width: 25px;\n"
                           "}\n"
                           "QScrollBar::add-line:horizontal {\n"
                           "  	border: 1px solid rgb(207,207,207);\n"
                           "  	border-top-right-radius: 7px;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	border-bottom-right-radius: 7px;\n"
                           "  	background: rgb(255, 255, 255);\n"
                           "  	width: 20px;\n"
                           "  	subcontrol-position: right;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::add-line:horizontal:hover {\n"
                           "  	border: 1px solid rgb(255,150,60);\n"
                           "  	border-top-right-radius: 7px;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	border-bottom-right-radius: 7px;\n"
                           "  	background: rgb(255, 255, 255);\n"
                           "  	width: 20px;\n"
                           "  	subcontrol-position: right;\n"
                           "  	subcontro"
                           "l-origin: margin;\n"
                           "}\n"
                           "QScrollBar::add-line:horizontal:pressed {\n"
                           "  	border: 1px solid grey;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	border-top-right-radius: 7px;\n"
                           "  	border-bottom-right-radius: 7px;\n"
                           "  	background: rgb(231,231,231);\n"
                           "  	width: 20px;\n"
                           "  	subcontrol-position: right;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::sub-line:horizontal {\n"
                           "  	border: 1px solid rgb(207,207,207);\n"
                           "  	border-top-right-radius: 7px;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	border-bottom-left-radius: 7px;\n"
                           "  	background: rgb(255, 255, 255);\n"
                           "  	width: 20px;\n"
                           "  	subcontrol-position: left;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::sub-line:horizontal:hover {\n"
                           "  	border: 1px solid rgb(255,150,60);\n"
                           "  	border-top-right-radius: 7px;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	border-bottom-left-radius: 7px;\n"
                           "  	background: rgb(255, 255, 255);\n"
                           "  	width: 20px;\n"
                           "  	subcontrol-position: left;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::sub-li"
                           "ne:horizontal:pressed {\n"
                           "  	border: 1px solid grey;\n"
                           "  	border-top-right-radius: 7px;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	border-bottom-left-radius: 7px;\n"
                           "  	background: rgb(231,231,231);\n"
                           "  	width: 20px;\n"
                           "  	subcontrol-position: left;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::left-arrow:horizontal {\n"
                           "  	border: 1px transparent grey;\n"
                           "  	border-top-left-radius: 3px;\n"
                           "  	border-bottom-left-radius: 3px;\n"
                           "  	width: 6px;\n"
                           "  	height: 6px;\n"
                           "  	background: rgb(230,230,230);\n"
                           "}\n"
                           "QScrollBar::right-arrow:horizontal {\n"
                           "	border: 1px transparent grey;\n"
                           "	border-top-right-radius: 3px;\n"
                           "	border-bottom-right-radius: 3px;\n"
                           "  	width: 6px;\n"
                           "  	height: 6px;\n"
                           " 	background: rgb(230,230,230);\n"
                           "}\n"
                           "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                           " 	background: none;\n"
                           "} \n"
                           "QScrollBar:vertical {\n"
                           "	max-width: 20px;\n"
                           "	border: 1px transparent grey;\n"
                           "	margin: 20px 0px 20px 0px;\n"
                           "}\n"
                           "QScrollBar::add-line:vertical {\n"
                           ""
                           "	border: 1px solid;\n"
                           "	border-color: rgb(207,207,207);\n"
                           "	border-bottom-right-radius: 7px;\n"
                           "	border-bottom-left-radius: 7px;\n"
                           "	border-top-left-radius: 7px;\n"
                           "	background: rgb(255, 255, 255);\n"
                           "  	height: 20px;\n"
                           "  	subcontrol-position: bottom;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::add-line:vertical:hover {\n"
                           "  	border: 1px solid;\n"
                           "  	border-color: rgb(255,150,60);\n"
                           "  	border-bottom-right-radius: 7px;\n"
                           "  	border-bottom-left-radius: 7px;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	background: rgb(255, 255, 255);\n"
                           "  	height: 20px;\n"
                           "  	subcontrol-position: bottom;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::add-line:vertical:pressed {\n"
                           "  	border: 1px solid grey;\n"
                           "  	border-bottom-left-radius: 7px;\n"
                           "  	border-bottom-right-radius: 7px;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	background: rgb(231,231,231);\n"
                           "  	height: 20px;\n"
                           "  	subcontrol-position: bottom;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::sub-line:vertical {\n"
                           "  	b"
                           "order: 1px solid rgb(207,207,207);\n"
                           "  	border-top-right-radius: 7px;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	border-bottom-left-radius: 7px;\n"
                           "  	background: rgb(255, 255, 255);\n"
                           "  	height: 20px;\n"
                           "  	subcontrol-position: top;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::sub-line:vertical:hover {\n"
                           "  	border: 1px solid rgb(255,150,60);\n"
                           "  	border-top-right-radius: 7px;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	border-bottom-left-radius: 7px;\n"
                           "	background: rgb(255, 255, 255);\n"
                           "  	height: 20px;\n"
                           "  	subcontrol-position: top;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::sub-line:vertical:pressed {\n"
                           "  	border: 1px solid grey;\n"
                           "  	border-top-left-radius: 7px;\n"
                           "  	border-top-right-radius: 7px;\n"
                           "  	background: rgb(231,231,231);\n"
                           " 	height: 20px;\n"
                           "  	subcontrol-position: top;\n"
                           "  	subcontrol-origin: margin;\n"
                           "}\n"
                           "QScrollBar::handle:vertical {\n"
                           "	background: rgb(253,253,253);\n"
                           "	border: 1px solid rgb(207,207,207);\n"
                           "	border-radius: 7px;\n"
                           "	"
                           "min-height: 25px;\n"
                           "}\n"
                           "QScrollBar::handle:vertical:hover {\n"
                           "	background: rgb(253,253,253);\n"
                           "	border: 1px solid rgb(255,150,60);\n"
                           "	border-radius: 7px;\n"
                           "	min-height: 25px;\n"
                           "}\n"
                           "QScrollBar::up-arrow:vertical {\n"
                           "	border: 1px transparent grey;\n"
                           "  	border-top-left-radius: 3px;\n"
                           "	border-top-right-radius: 3px;\n"
                           "  	width: 6px;\n"
                           "  	height: 6px;\n"
                           "  	background: rgb(230,230,230);\n"
                           "}\n"
                           "QScrollBar::down-arrow:vertical {\n"
                           "  	border: 1px transparent grey;\n"
                           "  	border-bottom-left-radius: 3px;\n"
                           "  	border-bottom-right-radius: 3px;\n"
                           "  	width: 6px;\n"
                           "  	height: 6px;\n"
                           "  	background: rgb(230,230,230);\n"
                           "}\n"
                           "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                           "  	background: none;\n"
                           "}\n"
                           "QTabWidget {\n"
                           "	color:rgb(0,0,0);\n"
                           "	background-color:rgb(247,246,246);\n"
                           "}\n"
                           "QTabWidget::pane {\n"
                           "	border-color: rgb(180,180,180);\n"
                           "	background-color:rgb(247,246,246);\n"
                           "	border-style: solid;\n"
                           "	border-width: 1px;\n"
                           "  	border-radius: 6px;\n"
                           "}\n"
                           "Q"
                           "TabBar::tab {\n"
                           "	padding-left:4px;\n"
                           "	padding-right:4px;\n"
                           "	padding-bottom:2px;\n"
                           "	padding-top:2px;\n"
                           "	color:rgb(81,72,65);\n"
                           "  	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(221,218,217,255), stop:1 rgba(240,239,238,255));\n"
                           "	border-style: solid;\n"
                           "	border-width: 1px;\n"
                           "  	border-top-right-radius:4px;\n"
                           "	border-top-left-radius:4px;\n"
                           "	border-top-color: rgb(180,180,180);\n"
                           "	border-left-color: rgb(180,180,180);\n"
                           "	border-right-color: rgb(180,180,180);\n"
                           "	border-bottom-color: transparent;\n"
                           "}\n"
                           "QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {\n"
                           "  	background-color:rgb(247,246,246);\n"
                           "  	margin-left: 0px;\n"
                           "  	margin-right: 1px;\n"
                           "}\n"
                           "QTabBar::tab:!selected {\n"
                           "	margin-top: 1px;\n"
                           "	margin-right: 1px;\n"
                           "}\n"
                           "QTextEdit {\n"
                           "	border-width: 1px;\n"
                           "	border-style: solid;\n"
                           "	border-color:transparent;\n"
                           "	color:rgb(17,17,17);\n"
                           "	selection-background-color:rgb(236,116,64);\n"
                           "}\n"
                           "QTimeEdit, QToolBox, "
                           "QToolBox::tab, QToolBox::tab:selected {\n"
                           "	color:rgb(81,72,65);\n"
                           "	background-color: #ffffff;\n"
                           "}")

        # 初始化数据库
        with sqlite3.connect('files/birthday.db') as self.conn:
            self.cursor = self.conn.cursor()
            self.create_table()
            self.ensure_reminded_today_column()
            self.reset_reminded_today()

        # 初始化界面
        self.init_ui()

        # 定时检查生日
        self.check_birthdays_interval()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                birthday TEXT,
                type TEXT,
                reminded_today INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def ensure_reminded_today_column(self):
        self.cursor.execute("PRAGMA table_info(contacts)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if 'reminded_today' not in columns:
            self.cursor.execute("ALTER TABLE contacts ADD COLUMN reminded_today INTEGER DEFAULT 0")
            self.conn.commit()

    def reset_reminded_today(self):
        self.cursor.execute("UPDATE contacts SET reminded_today = 0")
        self.conn.commit()

    def init_ui(self):
        # 创建主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建联系人表格
        self.contacts_table = QTableWidget()
        self.contacts_table.setRowCount(0)
        self.contacts_table.setColumnCount(4)
        self.contacts_table.setHorizontalHeaderLabels(["姓名", "生日", "类型", "年龄"])
        self.contacts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contacts_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contacts_table.itemSelectionChanged.connect(self.enable_buttons)
        layout.addWidget(self.contacts_table)

        # 创建按钮布局
        button_layout = QGridLayout()

        # 添加按钮
        self.add_button = QPushButton("添加联系人")
        self.add_button.clicked.connect(self.add_contact)
        button_layout.addWidget(self.add_button, 0, 0)

        # 编辑按钮
        self.edit_button = QPushButton("编辑联系人")
        self.edit_button.clicked.connect(self.edit_contact)
        self.edit_button.setEnabled(False)
        button_layout.addWidget(self.edit_button, 0, 1)

        # 删除按钮
        self.delete_button = QPushButton("删除联系人")
        self.delete_button.clicked.connect(self.delete_contact)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button, 0, 2)

        # 检查今天谁生日按钮
        self.check_today_button = QPushButton("检查今天谁生日")
        self.check_today_button.clicked.connect(self.check_today_birthdays)
        button_layout.addWidget(self.check_today_button, 0, 3)

        layout.addLayout(button_layout)

        # 刷新联系人列表
        self.refresh_contacts()

    def refresh_contacts(self):
        self.contacts_table.setRowCount(0)
        self.contacts = self.get_contacts()
        for row, contact in enumerate(self.contacts):
            age = self.calculate_age(contact[2], contact[3])
            self.contacts_table.insertRow(row)
            self.contacts_table.setItem(row, 0, QTableWidgetItem(contact[1]))
            self.contacts_table.setItem(row, 1, QTableWidgetItem(contact[2]))
            self.contacts_table.setItem(row, 2, QTableWidgetItem(contact[3]))
            self.contacts_table.setItem(row, 3, QTableWidgetItem(str(age)))

    def enable_buttons(self):
        selected_items = self.contacts_table.selectedItems()
        self.edit_button.setEnabled(bool(selected_items))
        self.delete_button.setEnabled(bool(selected_items))

    def calculate_age(self, birthday_str, type_):
        try:
            if type_ == "国历":
                birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
            else:
                birthday = self.lunar_to_solar(birthday_str)
            age = datetime.now().year - birthday.year
        except ValueError:
            age = 0
        return age

    def lunar_to_solar(self, lunar_str):
        year, month, day = map(int, lunar_str.split('-'))
        lunar = sxtwl.fromLunar(year, month, day)
        solar = sxtwl.fromSolar(lunar.getSolarYear(), lunar.getSolarMonth(), lunar.getSolarDay())
        return datetime(solar.getSolarYear(), solar.getSolarMonth(), solar.getSolarDay())

    def add_contact(self):
        name, ok = QInputDialog.getText(self, "添加联系人", "姓名:")
        if ok and name:
            birthday_str = self.get_date("添加联系人", "选择生日")
            if birthday_str:
                type_ = self.get_type("添加联系人", "生日类型")
                if type_ in ["农历", "国历"]:
                    with sqlite3.connect('files/birthday.db') as conn:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO contacts (name, birthday, type) VALUES (?,?,?)",
                                       (name, birthday_str, type_))
                        conn.commit()
                    self.refresh_contacts()
                else:
                    QMessageBox.warning(self, "警告", "生日类型必须是'农历'或'国历'")
            else:
                QMessageBox.warning(self, "警告", "请选择有效的日期")
        else:
            QMessageBox.warning(self, "警告", "请输入有效内容")

    def edit_contact(self):
        selected_row = self.contacts_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个联系人")
            return

        selected_id = self.contacts_table.item(selected_row, 0).text()
        name, ok = QInputDialog.getText(self, "编辑联系人", "新姓名:", text=selected_id)
        if ok and name:
            birthday_str = self.get_date("编辑联系人", "选择新生日")
            if birthday_str:
                type_ = self.get_type("编辑联系人", "新生日类型")
                if type_ in ["农历", "国历"]:
                    with sqlite3.connect('files/birthday.db') as conn:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE contacts SET name =?, birthday =?, type =? WHERE name =?",
                                       (name, birthday_str, type_, selected_id))
                        conn.commit()
                    self.refresh_contacts()
                else:
                    QMessageBox.warning(self, "警告", "生日类型必须是'农历'或'国历'")
            else:
                QMessageBox.warning(self, "警告", "请选择有效的日期")
        else:
            QMessageBox.warning(self, "警告", "请输入有效内容")

    def delete_contact(self):
        selected_row = self.contacts_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个联系人")
            return

        selected_id = self.contacts_table.item(selected_row, 0).text()
        reply = QMessageBox.question(self, "确认删除", "确定要删除这个联系人吗？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            with sqlite3.connect('files/birthday.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM contacts WHERE name =?", (selected_id,))
                conn.commit()
            self.refresh_contacts()

    def check_birthdays(self, remind_today=True):
        solartoday = datetime.now().strftime("%m-%d")
        solartoday3 = datetime.now().strftime("%Y-%m-%d")
        solartoday2 = datetime.strptime(solartoday3, "%Y-%m-%d")
        day = sxtwl.fromSolar(solartoday2.year, solartoday2.month, solartoday2.day)
        lunar = sxtwl.fromSolar(day.getLunarYear(), day.getLunarMonth(), day.getLunarDay())
        solar = sxtwl.fromLunar(lunar.getSolarYear(), lunar.getSolarMonth(), lunar.getSolarDay())
        lunartoday = f"{solar.getLunarMonth():02d}-{solar.getLunarDay():02d}"

        with sqlite3.connect('files/birthday.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contacts")
            contacts = cursor.fetchall()

        for contact in contacts:
            try:
                birthday = datetime.strptime(contact[2], "%Y-%m-%d").strftime("%m-%d")
            except ValueError:
                birthday = datetime.strptime(contact[2], "%m/%d/%y").strftime("%m-%d")
                with sqlite3.connect('files/birthday.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE contacts SET birthday =? WHERE id =?",
                                   (birthday, contact[0]))
                    conn.commit()

            if birthday == solartoday and (remind_today or contact[4] == 0) and contact[3] == '国历':
                age = datetime.now().year - datetime.strptime(contact[2], "%Y-%m-%d").year
                response = QMessageBox.question(self, "生日提醒", f"今天是{contact[1]}的生日！TA今天{age}岁了。\n今天不再提醒？",
                                                QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.Yes:
                    with sqlite3.connect('files/birthday.db') as conn:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE contacts SET reminded_today = 1 WHERE name =?", (contact[1],))
                        conn.commit()
            if birthday == lunartoday and (remind_today or contact[4] == 0) and contact[3] == '农历':
                age = datetime.now().year - datetime.strptime(contact[2], "%Y-%m-%d").year
                response = QMessageBox.question(self, "生日提醒", f"今天是{contact[1]}的生日！TA今天{age}岁了。\n今天不再提醒？",
                                                QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.Yes:
                    with sqlite3.connect('files/birthday.db') as conn:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE contacts SET reminded_today = 1 WHERE name =?", (contact[1],))
                        conn.commit()

    def check_today_birthdays(self):
        self.check_birthdays(remind_today=True)

    def check_birthdays_interval(self):
        self.check_birthdays()
        # 使用 QTimer 每天检查一次
        QTimer.singleShot(86400000, self.check_birthdays_interval)

    def get_contacts(self):
        with sqlite3.connect('files/birthday.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contacts")
            return cursor.fetchall()

    def get_date(self, title, prompt):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setWindowFlags(self.windowFlags() & ~(Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint))

        layout = QVBoxLayout(dialog)

        label = QLabel(prompt)
        layout.addWidget(label)

        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setSelectedDate(QDate(QDate.currentDate().year() - 16, QDate.currentDate().month(), QDate.currentDate().day()))
        calendar.setMaximumDate(QDate(QDate.currentDate().year(), QDate.currentDate().month(), QDate.currentDate().day() + 1))
        layout.addWidget(calendar)

        ok_button = QPushButton("确定")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)

        dialog.setLayout(layout)
        dialog.exec_()

        selected_date = calendar.selectedDate()
        return selected_date.toString("yyyy-MM-dd")

    def get_type(self, title, prompt):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setWindowFlags(self.windowFlags() & ~(Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint))

        layout = QVBoxLayout(dialog)

        label = QLabel(prompt)
        layout.addWidget(label)

        self.type_group = QButtonGroup(dialog)
        solar_radio = QRadioButton("国历")
        solar_radio.setChecked(True)
        lunar_radio = QRadioButton("农历")
        self.type_group.addButton(solar_radio, 0)
        self.type_group.addButton(lunar_radio, 1)

        layout.addWidget(solar_radio)
        layout.addWidget(lunar_radio)

        ok_button = QPushButton("确定")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)

        dialog.setLayout(layout)
        dialog.exec_()

        return "国历" if solar_radio.isChecked() else "农历"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BirthdayReminder()
    window.show()
    sys.exit(app.exec_())