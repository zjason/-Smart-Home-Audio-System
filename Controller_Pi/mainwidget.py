from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget
from ui_smart_central import Ui_Form


class MainWidget(QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Smart Console')
        self.setFixedSize(self.size())


