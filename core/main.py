import functools
import os
import json
import pathlib
from enum import Enum

from PyQt5 import (
    uic,
    QtWebEngineWidgets,
    QtWebChannel,
    QtCore,
    QtWidgets,
)
from PyQt5.QtCore import QSortFilterProxyModel, Qt


class Config:

    CRS_DATA_JSON = "data/crs.json"
    UNITS_DATA_JSON = "data/units.json"


class CrsType(Enum):

    Projected = "projected"
    Geographic2d = 'geographic 2d'
    Geographic3d = 'geographic 3d'
    Compound = 'compound'
    Vertical = 'vertical'


class MainWindow(QtWidgets.QMainWindow):
    comboBoxCrsInH: QtWidgets.QComboBox
    comboBoxCrsInV: QtWidgets.QComboBox
    comboBoxCrsOutH: QtWidgets.QComboBox
    comboBoxCrsOutV: QtWidgets.QComboBox
    comboBoxUnitsOutV: QtWidgets.QComboBox
    comboBoxUnitsOutH: QtWidgets.QComboBox
    comboBoxUnitsInV: QtWidgets.QComboBox
    comboBoxUnitsInH: QtWidgets.QComboBox
    comboBoxGeoidInH: QtWidgets.QComboBox
    comboBoxGeoidOutH: QtWidgets.QComboBox
    tabWidgetInputCrs: QtWidgets.QTabWidget
    tabWidgetOutputCrs: QtWidgets.QTabWidget
    pushButtonConvert: QtWidgets.QPushButton
    tableWidgetInCrs: QtWidgets.QTableWidget
    tableWidgetOutCrs: QtWidgets.QTableWidget

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

        # panToParis = functools.partial(self.panMap, 2.3272, 48.8620)
        # self.pushButton.clicked.connect(panToParis)

        self.setup_crs_combobox()
        self.setup_units_combobox()

        # crs signals
        self.comboBoxCrsInH.currentIndexChanged.connect(lambda: self.crs_changed(self.comboBoxCrsInH, self.comboBoxUnitsInH))
        self.comboBoxCrsOutH.currentIndexChanged.connect(lambda: self.crs_changed(self.comboBoxCrsOutH, self.comboBoxUnitsOutH))
        self.comboBoxCrsInV.currentIndexChanged.connect(lambda: self.crs_changed(self.comboBoxCrsInV, self.comboBoxUnitsInV))
        self.comboBoxCrsOutV.currentIndexChanged.connect(lambda: self.crs_changed(self.comboBoxCrsOutV, self.comboBoxUnitsOutV))
        # TODO set default crs

        self.pushButtonConvert.clicked.connect(lambda: self.convert_coord())

    def convert_coord(self):
        self.tableWidgetOutCrs.clearContents()
        # TODO need to clear rows in tableWidgetOutCrs
        for row in range(self.tableWidgetInCrs.rowCount()):
            x = self.tableWidgetInCrs.item(row, 0).text()
            y = self.tableWidgetInCrs.item(row, 1).text()
            z = self.tableWidgetInCrs.item(row, 2).text()
            print((x, y, z))
            self.tableWidgetOutCrs.insertRow(row)
            self.tableWidgetOutCrs.setItem(row, 0, QtWidgets.QTableWidgetItem(x))
            self.tableWidgetOutCrs.setItem(row, 1, QtWidgets.QTableWidgetItem(y))
            self.tableWidgetOutCrs.setItem(row, 2, QtWidgets.QTableWidgetItem(z))


    def crs_changed(self, crs_combobox: QtWidgets.QComboBox, unit_combobox: QtWidgets.QComboBox):
        # populate units depends on the crs
        current_data = crs_combobox.currentData()
        print(crs_combobox.objectName())
        unit_data = f"{current_data['units']['auth_name']}:{current_data['units']['code']}"
        unit_combobox.setCurrentIndex(unit_combobox.findData(unit_data, flags=QtCore.Qt.MatchFixedString))

    @QtCore.pyqtSlot(float, float)
    def onMapMove(self, lat, lng):
        self.label.setText("Lng: {:.5f}, Lat: {:.5f}".format(lng, lat))

    def panMap(self, lng, lat):
        page = self.view.page()
        page.runJavaScript("map.setView([{}, {}], 10);".format(lat, lng))
        page.runJavaScript("map.panTo(L.latLng({}, {}));".format(lat, lng))

    def setup_crs_combobox(self):
        # self.comboBoxCrsInH.currentTextChanged.connect(self.filter_compobox)
        full_path = pathlib.Path(Config.CRS_DATA_JSON)
        crss = json.loads(full_path.read_text())

        for crs in crss:
            crs_str = f"{crs['auth_name']}:{crs['code']} {crs['name']}"
            if crs["type"] in ["projected", "geographic 2d"]:
                self.comboBoxCrsInH.addItem(
                    crs_str,
                    {
                        "auth_name": crs["auth_name"],
                        "code": crs["code"],
                        "type": crs["type"],
                        "units": crs["h_units"],
                    },
                )
                self.comboBoxCrsOutH.addItem(
                    crs_str,
                    {
                        "auth_name": crs["auth_name"],
                        "code": crs["code"],
                        "type": crs["type"],
                        "units": crs["h_units"],
                    },
                )
            if crs["type"] in ["vertical", "geographic 3d"]:
                self.comboBoxCrsInV.addItem(
                    crs_str,
                    {
                        "auth_name": crs["auth_name"],
                        "code": crs["code"],
                        "type": crs["type"],
                        "units": crs["v_units"],
                    },
                )
                self.comboBoxCrsOutV.addItem(
                    crs_str,
                    {
                        "auth_name": crs["auth_name"],
                        "code": crs["code"],
                        "type": crs["type"],
                        "units": crs["v_units"],
                    },
                )

    def setup_units_combobox(self):
        full_path = pathlib.Path(Config.UNITS_DATA_JSON)
        units = json.loads(full_path.read_text())
        for unit in units:
            data = f"{unit['auth_name']}:{unit['code']}"
            unit_name = f"{unit['name']}  ({unit['linear_units_conv']} m)"
            self.comboBoxUnitsInH.addItem(unit_name, data)
            self.comboBoxUnitsOutH.addItem(unit_name, data)
            self.comboBoxUnitsInV.addItem(unit_name, data)
            self.comboBoxUnitsOutV.addItem(unit_name, data)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
