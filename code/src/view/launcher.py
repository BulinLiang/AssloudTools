import PyMVCS
from service.auth import AuthService
from facade.launcher import LauncherFacade
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence


class LauncherView(PyMVCS.View):
    NAME = 'LauncherView'

    def _setup(self):
        self.logger.Trace('LauncherView.setup')
        self.__launcherFacade = PyMVCS.UIFacade.Find(LauncherFacade.NAME)
        self.__ui = self.__launcherFacade.ui
        self.__window = self.__launcherFacade.window
        self.__window.show()
        # 禁止调整窗口大小
        self.__window.setFixedSize(self.__window.width(), self.__window.height())

        self.Route('/auth/token/update', self.handleSigninSuccess)
        self.Route('/auth/login/error', self.handleSigninError)

        # 绑定事件
        self.__ui.pbSignin.clicked.connect(self.onSigninClick)

        '''
            使用self.__ui.pbSignin.setShortcut(Qt.Key_Enter)设置快捷键，同时只能设置一个，所以要自定义快捷键的信号槽
            xxx = QShortcut(QKeySequence(快捷键), 继承的窗体控件)
            activated信号绑定槽函数
            xxx.activated.connect(self.onSigninClick)
        '''
        enter_short = QShortcut(QKeySequence(Qt.Key_Enter), self.__window)
        enter_short.activated.connect(self.onSigninClick)
        return_short = QShortcut(QKeySequence(Qt.Key_Return), self.__window)
        return_short.activated.connect(self.onSigninClick)

    def _dismantle(self):
        self.logger.Trace('LauncherView.dismantle')

    def onSigninClick(self):
        # TODO 登录加载如何实现
        self.logger.Trace('click signin')
        service = self.serviceCenter.Find(AuthService.NAME)
        username = self.__ui.leUsername.text()
        password = self.__ui.lePassword.text()
        url = self.__ui.leUrl.text()
        service.Signin(username, password, url)

    def handleSigninSuccess(self, _status, _data):
        self.logger.Trace('LauncherView.handleSigninSuccess')
        self.__launcherFacade.window.close()

    def handleSigninError(self, _status, _data):
        self.logger.Trace('LauncherView.handleSigninError')
        self.__ui.lbMessage.setText(_status.message)
