from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QLineEdit
from scripts.envVars import ADMIN_PASSWORD, PASSWORD, formLoginWindow, baseLoginWindow


class Login(formLoginWindow, baseLoginWindow):
    def __init__(self, main_window):
        main_window.logDebug.info("Call:Login.__init__()")
        super(baseLoginWindow, self).__init__()
        self.setupUi(self)
        self.__pwin = main_window
        self.label.setText("")
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(self.check_password)
        self.__pwin.logDebug.info("Return:Login.__init__()")

    def check_password(self):
        self.__pwin.logDebug.info("Call:Login.check_password()")
        if self.lineEdit.text().encode() == ADMIN_PASSWORD:
            self.__pwin.logInfo.info("ADMIN LOGIN GRANTED")
            self.__pwin.is_admin = True
            self.__pwin.child_window = None
        elif self.lineEdit.text().encode() == PASSWORD:
            self.__pwin.logInfo.info("LOGIN GRANTED")
            self.__pwin.child_window = None
        else:
            # self.__pwin.logInfo.info(f"LOGIN FAILED:{self.lineEdit.text()}")
            self.__pwin.logInfo.info("LOGIN FAILED")
            self.label.setText("Pogrešna lozinka!")
        self.__pwin.logDebug.info("Return:Login.check_password()")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.check_password()

    def closeEvent(self, event):
        self.__pwin.close()
        event.accept()
