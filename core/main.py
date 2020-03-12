import functools
import os
import json
import pathlib

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


class ExtendedComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QtWidgets.QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)


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
        self.setup_units_combobox()

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
        # self.comboBoxCrsInH.hide()
        # combo = ExtendedComboBox(self.tabCrsInHV)
        # combo.setGeometry(QtCore.QRect(10, 40, 201, 31))
        # combo.setEditable(True)
        # combo.setObjectName("comboBoxCrsH")
        # self.comboBoxCrsInH = combo

        for crs in crss:
            crs_str = f"{crs['auth_name']}:{crs['code']} {crs['name']}"
            if crs["type"] in ["projected", "geographic 2d"]:
                self.comboBoxCrsInH.addItem(
                    crs_str, {"auth_name": crs["auth_name"], "code": crs["code"]}
                )
                self.comboBoxCrsOutH.addItem(
                    crs_str, {"auth_name": crs["auth_name"], "code": crs["code"]}
                )
            if crs["type"] in ["vertical", "geographic 3d"]:
                self.comboBoxCrsInV.addItem(
                    crs_str, {"auth_name": crs["auth_name"], "code": crs["code"]}
                )
                self.comboBoxCrsOutV.addItem(
                    crs_str, {"auth_name": crs["auth_name"], "code": crs["code"]}
                )

    def setup_units_combobox(self):
        full_path = pathlib.Path(Config.UNITS_DATA_JSON)
        units = json.loads(full_path.read_text())
        for unit in units:
            unit_name = f"{unit['name']}  ({unit['linear_units_conv']} m)"
            self.comboBoxUnitsInH.addItem(unit_name, unit)
            self.comboBoxUnitsOutH.addItem(unit_name, unit)
            self.comboBoxUnitsInV.addItem(unit_name, unit)
            self.comboBoxUnitsOutV.addItem(unit_name, unit)

    def filter_compobox(self):
        print("changed")



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
