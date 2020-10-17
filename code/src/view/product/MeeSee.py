import PyMVCS
from facade.app import AppFacade
from model.product.MeeSee import MeeSeeProductModel
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QCheckBox, QAbstractItemView
from PyQt5.QtCore import Qt, QVariant, QFileInfo, QSize
from view.util import Util
import re


class MeeSeeProductView(PyMVCS.View):
    NAME = 'MeeSeeProductView'

    def _setup(self):
        self.logger.Trace('MeeSeeProductView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(MeeSeeProductModel.NAME)

        "MeeSee菜单"
        self.__ui.rbMeeSee.toggled.connect(self.onTabToggle)

    def _dismantle(self):
        self.logger.Trace('MeeSeeProductView.dismantle')

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageMeeSee)

