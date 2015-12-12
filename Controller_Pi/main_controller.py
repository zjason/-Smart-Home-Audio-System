from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QPointF, QTimer
from mainwidget import MainWidget
from ControllerGui import *
from PyQt5.QtGui import QTextCursor


class MainController(QObject):

    appstart = pyqtSignal()

    def __init__(self):
        super(MainController, self).__init__()
        self.mainWidget = MainWidget()
        self.ControllerCommunication = ControllerCommunication()
        self.ControllerCommunication._consumingThread_()

        self.ControllerCommunication.Room1_led.connect(self.change_led_text1)
        self.ControllerCommunication.Room2_led.connect(self.change_led_text2)

        self.ControllerCommunication.Room1_music_track_name.connect(self.update_track_name1)
        self.ControllerCommunication.Room2_music_track_name.connect(self.update_track_name2)

        self.ControllerCommunication.Room1_music_status.connect(self.update_track_status1)
        self.ControllerCommunication.Room2_music_status.connect(self.update_track_status2)

        # self.ControllerCommunication.Room1_led_On_Msg.connect(self.update_text_led_on)
        # self.ControllerCommunication.Room2_led_On_Msg.connect(self.update_text_led2_on)
        #
        # self.ControllerCommunication.Room1_led_Off_Msg.connect(self.update_text_led_off)
        # self.ControllerCommunication.Room2_led_Off_Msg.connect(self.update_text_led2_off)

        self.ControllerCommunication.Room1_music_volume.connect(self.update_room1_volume)
        self.ControllerCommunication.Room2_music_volume.connect(self.update_room2_volume)


        self.mainWidget.ui.pushButton_5.clicked.connect(self.clear_text)

    """
        Updating GUI elements for room 1

                                        _
                                      /' )
                                     (_, |
                                       | |
                                       | |
                                       (_)
    """
    @pyqtSlot(str)
    def change_led_text1(self, led1_status):
        """
        change led text for room 1
        :param led1_status:
        :return:
        """
        self.mainWidget.ui.pushButton.setText(led1_status)
        self.mainWidget.ui.textEdit.insertPlainText("Turned room 1 light " + led1_status + " !")
        self.mainWidget.ui.textEdit.moveCursor(QTextCursor.Start)


    @pyqtSlot(str)
    def update_track_name1(self, track1_name):
        """
        change music track name for room 1
        :param track1_name:
        :return:
        """
        self.mainWidget.ui.music_track_name_label.setText(track1_name)
        self.mainWidget.ui.textEdit.insertPlainText("Room 1 playing " + track1_name + "...")
        self.mainWidget.ui.textEdit.moveCursor(QTextCursor.Start)

    @pyqtSlot(str)
    def update_track_status1(self, track1_status):
        """
        change music status name for room 2
        :param track1_status:
        :return:
        """
        self.mainWidget.ui.music_label_status.setText(track1_status)

    """
        Updating GUI elements for room 2

                                       __
                                     /'__`\
                                    (_)  ) )
                                       /' /
                                     /' /( )
                                    (_____/'
    """

    @pyqtSlot(str)
    def change_led_text2(self, led2_status):
        """
        change led text for room 2
        :param led2_status:
        :return:
        """
        self.mainWidget.ui.pushButton_2.setText(led2_status)
        self.mainWidget.ui.textEdit.insertPlainText("Turned room 2 light " + led2_status + " !")
        self.mainWidget.ui.textEdit.moveCursor(QTextCursor.Start)

    @pyqtSlot(str)
    def update_track_name2(self, track2_name):
        """
        change music status name for room 2
        :param track2_name:
        :return:
        """
        self.mainWidget.ui.music_track_name_label_2.setText(track2_name)
        self.mainWidget.ui.textEdit.insertPlainText("Room 2 playing " + track2_name + "...")
        self.mainWidget.ui.textEdit.moveCursor(QTextCursor.Start)


    @pyqtSlot(str)
    def update_track_status2(self, track2_status):
        """
        change music status name for room 2
        :param track2_status:
        :return:
        """
        self.mainWidget.ui.music_label_status_2.setText(track2_status)

    @pyqtSlot(int)
    def update_room1_volume(self, num):
        self.mainWidget.ui.lcdNumber.display(num)

    @pyqtSlot(int)
    def update_room2_volume(self, num2):
        self.mainWidget.ui.lcdNumber_2.display(num2)

    # @pyqtSlot()
    # def update_text_led_on(self):
    #     self.mainWidget.ui.textBrowser.append("Turned room 1 light on !")
    #
    # @pyqtSlot()
    # def update_text_led2_on(self):
    #     self.mainWidget.ui.textBrowser.append("Turned room 2 light on !")
    #
    # @pyqtSlot()
    # def update_text_led_off(self):
    #     self.mainWidget.ui.textBrowser.append("Turned room 1 light off !")
    #
    # @pyqtSlot()
    # def update_text_led2_off(self):
    #     self.mainWidget.ui.textBrowser.append("Turned room 2 light off !")
    @pyqtSlot()
    def clear_text(self):
        self.mainWidget.ui.textEdit.clear()

    def start(self):
        self.mainWidget.show()
        self.mainWidget.showFullScreen()
        self.appstart.emit()
