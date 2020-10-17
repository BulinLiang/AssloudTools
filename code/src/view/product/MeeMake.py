import PyMVCS
from facade.app import AppFacade
from model.product.MeeMake import MeeMakeProductModel
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QCheckBox, QAbstractItemView
from PyQt5.QtCore import Qt, QVariant, QFileInfo, QSize
from view.util import Util
import re


class MeeMakeProductView(PyMVCS.View):
    NAME = 'MeeMakeProductView'

    def _setup(self):
        self.logger.Trace('MeeMakeProductView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(MeeMakeProductModel.NAME)

        "MeeMake菜单"
        self.__ui.rbMeeMake.toggled.connect(self.onTabToggle)


    def _dismantle(self):
        self.logger.Trace('MeeMakeProductView.dismantle')

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageMeeMake)

