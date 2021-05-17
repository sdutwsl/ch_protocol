
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton

class Login(QWidget):

    rgsSignal = pyqtSignal()    # 跳转至注册界面的信号
    settingSignal = pyqtSignal()
    statSignal = pyqtSignal(str)    # 更新面板状态栏的信号
    sendSignal = pyqtSignal(dict)   # 向服务器发送数据的信号
    cfSignal = pyqtSignal(str) # 跳转至主界面的信号
    portSignal = pyqtSignal(int)
    addrSignal = pyqtSignal(str)


    def __init__(self):
        super().__init__()

        self.initUI()


    # 绘制图形界面
    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        # 用户名输入
        lbu = QLabel('用户名：', self)
        self.ur = QLineEdit(self)
        grid.addWidget(lbu, 3, 0, 1, 2)
        grid.addWidget(self.ur, 3, 1, 1, 2)

        # 密码输入
        lbp = QLabel('密码：', self)
        self.pw = QLineEdit(self)
        self.pw.setEchoMode(QLineEdit.Password)
        grid.addWidget(lbp, 4, 0, 1, 1)
        grid.addWidget(self.pw, 4, 1, 1, 2)


        # 登录按钮
        bt1 = QPushButton('登录')
        grid.addWidget(bt1, 5, 2)
        bt1.clicked.connect(self.send)

        # 注册账号
        bt2 = QPushButton('注册账号')
        grid.addWidget(bt2, 5, 1)
        bt2.clicked.connect(self.go_rgs)

        bt3 = QPushButton('设置')
        grid.addWidget(bt3, 5, 0)
        bt3.clicked.connect(self.go_setting)

        # 设置布局
        self.setLayout(grid)


    # 将用户名与密码发送至服务器端
    def send(self):
        ur = self.ur.text()
        pw = self.pw.text()
        data = {'type': 'lg', 'cnt': {'ur': ur, 'pw': pw}}  # 定义传输数据结构
        self.sendSignal.emit(data)

    # 跳转至注册页面
    def go_rgs(self):
        self.close()
        self.rgsSignal.emit()

    def go_setting(self):
        self.settingSignal.emit()

    # 根据从服务器返回的结果执行相应操作
    def result(self, rs):
        if rs:  # 如果登录成功
            ur = self.ur.text()
            self.cfSignal.emit(ur)    # 发送跳转至主界面的信号
        else:
            self.ur.clear()
            self.pw.clear()