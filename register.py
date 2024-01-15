"""
https://github.com/Rovindu-Thamuditha/authentication-system

MIT License

Copyright (c) 2024 [Rovindu Thamuditha]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sqlite3
import sys
from PyQt5 import QtCore, uic
from authentication.authentication import login, register
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

conn = sqlite3.connect('users.db')

ALERT_MSG_BOX_STYLE = """
            QMessageBox {
                background-color: #252525;
                color: white;
            }
            QLabel {
                color: #aaa;
                padding-top: 18px;
                margin-top: 0;
                font-size: 16px;
                font-family: "sans-serif";
            }
            QLineEdit {
                background: #333;
                border: none;
                outline: none;
                color: #fff;
                height: 35px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: rgb(255, 255, 0);
                color: #252525;
                border-radius: 3px;
                height: 30px;
                width: 60px;
                padding: 4px 8px 4px 8px;
                font-size: 14px;
                margin-left: 0;
                font-family: "MS Shell Dlg 2", sans-serif;
            }
            QPushButton:hover {
                background-color: rgb(255, 255, 0, 0.8);
                border: 1px solid rgb(255, 255, 0);
            }
        """
class App(QMainWindow):
    def __init__(self):
        super().__init__()        
        uic.loadUi('gui/registerUi.ui', self)

        self.registerBtn.clicked.connect(self.register_user)
        self.registerBtn.setStyleSheet("""
        QPushButton {
            background-color: rgb(255, 255, 0);
            border-radius: 3px;
            height: 30px;
            padding: 4px 8px 4px 8px;
        }

        QPushButton:hover {
            background-color: rgb(255, 255, 0, 0.8) ;
            border: 1px solid  rgb(255, 255, 0);
        }
        """)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Make it a modal window
        #self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # Set the window to stay on top
        self.setFixedSize(self.size()) # Disbale Resizing

    def register_user(self):
        name = self.name.text()
        username = self.username.text()
        password = self.password.text()

        auth = register(username, name, password, password, conn)

        alert = QMessageBox()

        if auth['success']:
            alert.setIcon(QMessageBox.Information)
            alert.setWindowTitle("Registration Successful")
            alert.setText(f'Welcome {name} Here are your details \n\n{auth["message"]}')
            alert.setStyleSheet(ALERT_MSG_BOX_STYLE)
            button_clicked = alert.exec_()
            sys.exit(0)
        else:
            alert.setIcon(QMessageBox.Critical)
            alert.setWindowTitle("Registration Failed")
            alert.setText(f"{auth['message']} \n")

        alert.setSizeGripEnabled(False)  # Disable the size grip
        alert.setFixedSize(500, 150) 
        alert.setStyleSheet(ALERT_MSG_BOX_STYLE)
        button_clicked = alert.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())

conn.close()
