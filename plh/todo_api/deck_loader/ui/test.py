import sys

from PySide6 import QtCore, QtWidgets

from plh.hal.deck_loader.ui import deck_loading_guidance


class MainWindow(QtWidgets.QWidget, deck_loading_guidance.Ui_dlg):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)


app = QtWidgets.QApplication(sys.argv)
QtCore.QCoreApplication.instance()
window = MainWindow()
window.setWindowFlags(
    QtCore.Qt.WindowType.WindowMinimizeButtonHint,
)
window.show()
app.exec()
