import sys

from PyQt5 import QtWidgets

# Press the green button in the gutter to run the script.
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QSystemTrayIcon, QMenu

from ui.MainWindow import MainWindow


from PyQt5.QtCore import Qt, QFile, QTextStream

app = None

if __name__ == '__main__':
    # define ico

    # load the qt application
    app = QtWidgets.QApplication(sys.argv)
    tray_icon = QSystemTrayIcon(QIcon('media/icon.PNG'), parent=app)
    tray_icon.setToolTip('RNApp')
    tray_icon.show()

    # splash screen
    splash = QLabel()
    pixmap = QPixmap('media/logo/RN.png')
    # pixmap = pixmap.scaled(640, 640)
    splash.setPixmap(pixmap)
    splash.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    splash.show()

    # main window init

    window = MainWindow(app=app)
    window.setWindowIcon(QIcon('media/logo/RN.png'))
    # make tray menu
    menu = QMenu()
    exit_action = menu.addAction('Exit')
    exit_action.triggered.connect(window.close)

    # stylesheet init

    stylesheet = QFile('ui/stylesheet/dark.qss')
    stylesheet.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(stylesheet)
    app.setStyleSheet(stream.readAll())
    # splash screen destroy
    splash.destroy()

    window.show()
    app.exec_()
    print('Resuming Console Interaction.')

