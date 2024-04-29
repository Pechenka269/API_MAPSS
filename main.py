import sys
from pprint import pprint

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow
import requests
from PyQt6.QtCore import Qt
from PIL import Image
from io import BytesIO
from geocoder import get_ll_span, geocode


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.initUi()

    def initUi(self):
        self.type_map = 'map'
        self.lon = 39.558881  # широта
        self.lat = 50.199912  # долгота
        self.z = 16
        self.spn_lon = 0.005
        self.spn_lat = 0.005
        self.pt_lon = 0
        self.pt_lat = 0
        self.flag_point = False
        self.flag_mail = False
        self.get_image_map()
        self.radio_button_map.setChecked(1)
        self.restart_button.clicked.connect(self.restart)
        self.mail_index_box.toggled.connect(self.mail_index)
        for radio_button in self.map_group.buttons():
            radio_button.toggled.connect(self.set_map)
        self.find_button.clicked.connect(self.get_coord)

    def mail_index(self):
        self.flag_mail = not self.flag_mail
        self.get_coord()

    def restart(self):
        self.type_map = 'map'
        self.lon = 39.558881  # широта
        self.lat = 50.199912  # долгота
        self.z = 16
        self.spn_lon = 0.005
        self.spn_lat = 0.005
        self.pt_lon = 0
        self.pt_lat = 0
        self.radio_button_map.setChecked(1)
        self.flag_point = False
        self.edit_name.setText('')
        self.get_image_map()
        self.adress_label.setText('')
        self.flag_mail = False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
