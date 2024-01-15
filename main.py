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
import subprocess
from PyQt5 import QtCore, uic
from authentication.authentication import login, register
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout,QWidget, QLabel

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

class Authentication(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('assets/loginUi.ui', self)

        self.user_login_btn.setStyleSheet("""
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

        self.user_login_btn.clicked.connect(self.login_user)
        self.register_btn.mousePressEvent = self.register_user
        
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Make it a modal window
        #self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # Set the window to stay on top
        self.setFixedSize(self.size()) # Disbale Resizing

        self.show()
        self.setFocus()  # Set focus to the login window

    def register_user(self, event):
        # Launch the register.py script as a separate process
        process = subprocess.Popen(['python', 'register.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the subprocess to complete
        process.wait()


    def login_user(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        auth = login(username, password, conn)

        alert = QMessageBox()

        if auth['success']:
            alert.setIcon(QMessageBox.Information)
            alert.setWindowTitle("Login Successful")
            alert.setText(f'Welcome {username}')
            self.close()
            self.app = App()
            self.app.show()


        else:
            alert.setIcon(QMessageBox.Critical)
            alert.setWindowTitle("Authentication Failed")
            alert.setText(f"{auth['message']} \n")

        alert.setStyleSheet(ALERT_MSG_BOX_STYLE)
        alert.setSizeGripEnabled(False)  # Disable the size grip
        alert.setFixedSize(500, 150) 
        alert.exec_()


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello World")
        self.setGeometry(100, 100, 800, 600)  # Adjust the size and position as needed

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to this Window")
        welcome_label.setStyleSheet("font-size: 18px; color: #fff;")

        # Add more widgets and functionality as needed
        layout.addWidget(welcome_label)

        self.setLayout(layout)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Authentication()
    window.show()
    sys.exit(app.exec_())
