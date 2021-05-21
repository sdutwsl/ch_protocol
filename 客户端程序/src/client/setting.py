import configparser
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QApplication

from main_form import MForm


class Setting(QWidget):

    rgsSignal = pyqtSignal()    # 跳转至注册界面的信号
    statSignal = pyqtSignal(str)    # 更新面板状态栏的信号
    sendSignal = pyqtSignal(dict)   # 向服务器发送数据的信号
    cfSignal = pyqtSignal(str) # 跳转至主界面的信号
    portSignal = pyqtSignal(int)
    addrSignal = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.resize(290,190)
        self.lg_form = None
        self.initUI()

    # 绘制图形界面
    def initUI(self):
        self.setWindowTitle("设置")
        grid = QGridLayout()
        grid.setSpacing(10)

        #地址输入
        addr_l = QLabel('服务器地址: ', self)
        self.addr_in = QLineEdit(self)
        self.addr_in.setText("127.0.0.1")
        grid.addWidget(addr_l, 1, 0, 1, 2)
        grid.addWidget(self.addr_in, 1, 1, 1, 2)

        # 端口输入
        port_l = QLabel('端口: ', self)
        self.port_in = QLineEdit(self)
        self.port_in.setText("1234")
        grid.addWidget(port_l, 2, 0, 1, 2)
        grid.addWidget(self.port_in, 2, 1, 1, 2)


        # 登录按钮
        bt1 = QPushButton('记住设置(下次启动生效)')
        grid.addWidget(bt1, 5, 2)
        bt1.clicked.connect(self.remember_config)

        # 注册账号
        # bt2 = QPushButton('仅本次')
        # grid.addWidget(bt2, 5, 1)
        # bt2.clicked.connect(self.only_once)

        # 设置布局
        self.setLayout(grid)


    def remember_config(self):

        cp = configparser.ConfigParser()
        cp.read("chftp.cfg")
        addr = self.addr_in.text()
        port = self.port_in.text()
        cp.set('connection', 'addr', addr)
        cp.set('connection', 'port', port)
        cp.set('main', 'first_boot', '0')
        cp.write(open('chftp.cfg', 'w'))
        self.go_lg()

    def only_once(self):
        cp = configparser.ConfigParser()
        cp.read("chftp.cfg")
        addr = self.addr_in.text()
        port = self.port_in.text()
        cp.set('connection', 'addr', addr)
        cp.set('connection', 'port', port)
        cp.set('main', 'first_boot', '1')
        cp.write(open('chftp.cfg', 'w'))
        self.go_lg()


    def go_lg(self):
        self.close()
        if not self.lg_form:
            self.lg_form = MForm(setting_form=self)
            self.lg_form.show()
        else:
            self.lg_form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mf = Setting()
    mf.show()
    sys.exit(app.exec_())