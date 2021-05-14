import configparser
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from client.main_form import MForm

from client.setting import Setting

if __name__ == '__main__':
    QCoreApplication.addLibraryPath('.')
    app = QApplication(sys.argv)
    cp = configparser.ConfigParser()
    cp.read("chftp.cfg")
    setting_form = Setting()
    if cp.get('main', 'first_boot') == '1':
        setting_form.show()
    else:
        mf = MForm(setting_form=setting_form, host=cp.get('connection', 'addr'), port=int(cp.get('connection', 'port')))
        # mf = MForm(setting_form=setting_form)
        mf.show()
    sys.exit(app.exec_())