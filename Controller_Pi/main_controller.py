from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QPointF, QTimer
from mainwidget import MainWidget
from ControllerGui import *


class MainController(QObject):

    appstart = pyqtSignal()

    def __init__(self):
        super(MainController, self).__init__()
        self.mainWidget = MainWidget()
        self.ControllerCommunication = ControllerCommunication()
        self.ControllerCommunication.led.



    def start(self):
        self.mainWidget.show()
        self.appstart.emit()
