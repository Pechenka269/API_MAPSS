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

    def get_coord(self):
        if self.edit_name.text():
            _object_ = get_ll_span(self.edit_name.text())
            self.spn_lon, self.spn_lat = list(map(float, _object_[1].split(',')))
            self.lon, self.lat = list(map(float, _object_[0].split(',')))
            self.pt_lon, self.pt_lat = list(map(float, _object_[0].split(',')))
            self.flag_point = True
            self.get_image_map(flag=False)
            adress = geocode(self.edit_name.text())['metaDataProperty']['GeocoderMetaData']['Address']
            _adress_ = "\n".join(adress['formatted'].split(', '))
            if self.flag_mail:
                try:
                    mail_adress = adress['postal_code']
                    self.adress_label.setText(_adress_+f'\nпочтовый индекс: {mail_adress}')
                except KeyError:
                    self.adress_label.setText(_adress_)

            else:
                self.adress_label.setText(_adress_)
'''Жил-был в норе под землей хоббит. Не в какой-то там мерзкой
грязной сырой норе, где со всех сторон торчат хвосты червей и
противно пахнет плесенью, но и не в сухой песчаной голой норе, где
не на что сесть и нечего съесть. Нет, нора была хоббичья, а значит —
благоустроенная.
Она начиналась идеально круглой, как иллюминатор, дверью,
выкрашенной зеленой краской, с сияющей медной ручкой точно
посередине. Дверь отворялась внутрь, в длинный коридор, похожий на
железнодорожный туннель, но туннель без гари и без дыма и тоже
очень благоустроенный: стены там были обшиты панелями, пол
выложен плитками и устлан ковром, вдоль стен стояли полированные
стулья, и всюду были прибиты крючочки для шляп и пальто, так как
хоббит любил гостей. Туннель вился все дальше и дальше и заходил
довольно глубоко, но не в самую глубину Холма, как его именовали
жители на много миль в окружности. По обеим сторонам туннеля шли
двери — много-много круглых дверей. Хоббит не признавал
восхождений по лестницам: спальни, ванные, погреба, кладовые (целая
куча кладовых), гардеробные (хоббит отвел несколько комнат под
хранение одежды), кухни, столовые располагались в одном этаже и,
более того, в одном и том же коридоре.'''

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
