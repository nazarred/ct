import functools
import os
import sys
import json
import pathlib

from PyQt5 import (
    uic,
    QtGui,
    QtNetwork,
    QtWebEngineWidgets,
    QtWebChannel,
    QtCore,
    QtWidgets,
)
from PyQt5.QtCore import QUrl


class Config:

    CRS_DATA_JSON = "data/crs.json"


class MainWindow(QtWidgets.QMainWindow):
    comboBoxCrsH: QtWidgets.QComboBox
    comboBoxCrsV: QtWidgets.QComboBox

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("untitled.ui", self)

        self.setupUi()

    def setupUi(self):
        # self.setFixedSize(800, 500)
        self.verticalLayoutMap = self.verticalLayoutMap
        self.setLayout(self.verticalLayoutMap)

        label = self.label = QtWidgets.QLabel()
        sp = QtWidgets.QSizePolicy()
        sp.setVerticalStretch(0)
        label.setSizePolicy(sp)
        self.verticalLayoutMap.addWidget(label)
        view = self.view = QtWebEngineWidgets.QWebEngineView()
        channel = self.channel = QtWebChannel.QWebChannel()

        channel.registerObject("MainWindow", self)
        view.page().setWebChannel(channel)

        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "map.html",)
        self.view.setUrl(QtCore.QUrl.fromLocalFile(file))

        self.verticalLayoutMap.addWidget(view)

        panToParis = functools.partial(self.panMap, 2.3272, 48.8620)
        self.pushButton.clicked.connect(panToParis)
        self.setup_crs_combobox()

    @QtCore.pyqtSlot(float, float)
    def onMapMove(self, lat, lng):
        self.label.setText("Lng: {:.5f}, Lat: {:.5f}".format(lng, lat))

    def panMap(self, lng, lat):
        page = self.view.page()
        page.runJavaScript("map.setView([{}, {}], 10);".format(lat, lng))
        page.runJavaScript("map.panTo(L.latLng({}, {}));".format(lat, lng))

    def setup_crs_combobox(self):
        self.comboBoxCrsH.currentTextChanged.connect(self.filter_compobox)
        full_path = pathlib.Path(Config.CRS_DATA_JSON)
        crss = json.loads(full_path.read_text())
        for crs in crss:
            crs_str = f"{crs['auth_name']}:{crs['code']} {crs['name']}"
            if crs["type"] in ["projected", "geographic 2d"]:
                self.comboBoxCrsH.addItem(
                    crs_str, {"auth_name": crs["auth_name"], "code": crs["code"]}
                )
            if crs["type"] in ["vertical", "geographic 3d"]:
                self.comboBoxCrsV.addItem(
                    crs_str, {"auth_name": crs["auth_name"], "code": crs["code"]}
                )

    def filter_compobox(self):
        print("changed")



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
