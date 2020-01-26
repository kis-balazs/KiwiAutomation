from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import pyqtSlot
from my_kiwi import *


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.srcList = QLineEdit(self)
        self.dstList = QLineEdit(self)
        self.flyDate = QLineEdit(self)
        self.returnDate = QLineEdit(self)
        self.finishMessage = QMessageBox(self)
        self.button = QPushButton('Search flights', self)
        self.title = 'MyFlightRadar'
        self.left = 900
        self.top = 50
        self.width = 400
        self.height = 600
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create source textbox with info
        self.srcList.move(20, 20)
        self.srcList.setPlaceholderText("Insert the list of SRC airports, separated by comma")
        self.srcList.resize(280, 40)

        self.dstList.move(20, 80)
        self.dstList.setPlaceholderText("Insert the list of DST airports, separated by comma")
        self.dstList.resize(280, 40)

        self.flyDate.move(20, 140)
        self.flyDate.setPlaceholderText("Insert the start date, format: dd/mm/yyyy")
        self.flyDate.resize(280, 40)

        self.returnDate.move(20, 200)
        self.returnDate.setPlaceholderText("Insert the return date, format: dd/mm/yyyy")
        self.returnDate.resize(280, 40)

        # Create a button in the window
        self.button.move(20, 500)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot(name="search")
    def on_click(self):
        src = list(self.srcList.text().replace(" ", "").replace("\t", "").split(","))
        dst = list(self.dstList.text().replace(" ", "").replace("\t", "").split(","))
        from_date = str(self.flyDate.text())
        to_date = str(self.returnDate.text())
        dates = [from_date, to_date]
        # create the function call, with basic commands for now, exception-friendly
        try:
            fly_from_to(src=src, dst=dst, dates=dates, filters=[['fly_duration', 0]])
            # message the user that the process has finished, and clean up
            self.finishMessage.setWindowTitle("Successful search")
            self.finishMessage.setText("Search done, check file in flights folder")
            self.finishMessage.show()
            result = self.finishMessage.exec_()
            if result == 1024:
                self.close()
        except WIException as exc:
            self.finishMessage.setWindowTitle("Unsuccessful search")
            self.finishMessage.setText(str(exc))
            self.finishMessage.show()
        except Exception as exc:
            self.finishMessage.setWindowTitle("Other exception")
            self.finishMessage.setText(str(exc))
            self.finishMessage.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
