import PyMVCS
from facade.app import AppFacade
from PyQt5.QtCore import Qt, QSize
from PyQt5.Qt import QButtonGroup


class AppView(PyMVCS.View):
    NAME = 'AppView'

    def _setup(self):
        self.logger.Trace('AppView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__ui.swPages.setCurrentWidget(self.__facade.ui.pageWelcome)
        # self.__ui.swPages.setCurrentWidget(self.__facade.ui.pageMeeTouch)
        self._initialization()
        self._addRaidoInGroup()

        self.Route('/auth/token/update', self.handleSigninSuccess)

        # 菜单栏设置
        self.__ui.rbTerminal.toggled.connect(lambda: self.onTerminal(self.__ui.rbTerminal))
        self.__ui.rbFiles.toggled.connect(lambda: self.onFiles(self.__ui.rbFiles))
        self.__ui.rbCatalog.toggled.connect(lambda: self.onCatalog(self.__ui.rbCatalog))
        self.__ui.rbSourceMake.toggled.connect(lambda: self.onSourceMake(self.__ui.rbSourceMake))
        self.__ui.rbSet.toggled.connect(lambda: self.onSet(self.__ui.rbSet))
        self.__ui.rbAdmin.toggled.connect(lambda: self.onAdmin(self.__ui.rbAdmin))

    def _dismantle(self):
        self.logger.Trace('AppView.dismantle')

    def _initialization(self):
        self.__ui.fmTerminal.setHidden(True)
        # 文件
        self.__ui.fmFiles.setHidden(True)
        # 同步
        self.__ui.fmCatalog.setHidden(True)
        # 资源制作
        self.__ui.fmSourceMake.setHidden(True)
        # 设置
        self.__ui.fmSet.setHidden(True)
        # 管理员权限
        self.__ui.fmAdmin.setHidden(True)

    def _addRaidoInGroup(self):
        self.__ui.group_title = QButtonGroup()  # 创建按钮组
        self.__ui.group_title.addButton(self.__ui.rbTerminal, 0)
        self.__ui.group_title.addButton(self.__ui.rbFiles, 1)
        self.__ui.group_title.addButton(self.__ui.rbCatalog, 2)
        self.__ui.group_title.addButton(self.__ui.rbSourceMake, 3)
        self.__ui.group_title.addButton(self.__ui.rbSet, 4)
        self.__ui.group_title.addButton(self.__ui.rbAdmin, 5)
        # 设置组内按钮互斥
        self.__ui.group_title.setExclusive(True)

    def onTerminal(self, radio):
        if radio.text() == '终端产品':
            if radio.isChecked():
                self.__ui.fmTerminal.setHidden(False)
            else:
                self.__ui.fmTerminal.setHidden(True)

    def onFiles(self, radio):
        if radio.text() == '文件':
            if radio.isChecked():
                self.__ui.fmFiles.setHidden(False)
            else:
                self.__ui.fmFiles.setHidden(True)

    def onCatalog(self, radio):
        if radio.text() == '目录':
            if radio.isChecked():
                self.__ui.fmCatalog.setHidden(False)
            else:
                self.__ui.fmCatalog.setHidden(True)

    def onSet(self, radio):
        if radio.text() == '设置':
            if radio.isChecked():
                self.__ui.fmSet.setHidden(False)
            else:
                self.__ui.fmSet.setHidden(True)

    def onSourceMake(self, radio):
        if radio.text() == '资源制作':
            if radio.isChecked():
                self.__ui.fmSourceMake.setHidden(False)
            else:
                self.__ui.fmSourceMake.setHidden(True)

    def onAdmin(self, radio):
        if radio.text() == '超级管理员权限':
            if radio.isChecked():
                self.__ui.fmAdmin.setHidden(False)
            else:
                self.__ui.fmAdmin.setHidden(True)

    def handleSigninSuccess(self, _status, _data):
        self.logger.Trace('AppView.handleSigninSuccess')
        self.__facade.window.show()
