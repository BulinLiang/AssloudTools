import PyMVCS
from facade.app import AppFacade
from model.setting.Tools import ToolsSettingModel
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox
from PyQt5.QtCore import QSize
import os


class ToolsSettingView(PyMVCS.View):
    NAME = 'ToolsSettingView'

    def _setup(self):
        self.logger.Trace('ToolsSettingView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(ToolsSettingModel.NAME)

        self.Route('/setting/tools/pack/update', self.handleUpdatePackList)
        self.Route('/setting/tools/unpack/update', self.handleUpdateUnpackList)
        self.Route('/setting/tools/dynamic/update', self.handleUpdateDynamicList)
        self.Route('/setting/tools/clean', self.handleClean)

        "Tools菜单"
        self.__ui.rbAssistiveTools.toggled.connect(self.onTabToggle)
        self.__ui.rbAssistiveTools.clicked.connect(self.onTabClicke)

        "Pack打包"
        self.__ui.pbPackAddFiles.clicked.connect(self.onPackAddFiles)
        self.__ui.pbPackExportFiles.clicked.connect(self.onPackExportFiles)
        self.file_type = '.x2i'
        self.__ui.rbX2i.toggled.connect(lambda: self.buttonState(self.__ui.rbX2i))
        self.__ui.rbXma.toggled.connect(lambda: self.buttonState(self.__ui.rbXma))
        self.__ui.rbXsa.toggled.connect(lambda: self.buttonState(self.__ui.rbXsa))

        "Unpack解包"
        self.__ui.pbUnpackAddFiles.clicked.connect(self.onUnpackAddFiles)
        self.__ui.pbUnpackExportFiles.clicked.connect(self.onUnpackExportFiles)

        "Dynamic生成"
        self.__ui.pbDynamicAddFiles.clicked.connect(self.onDynamicAddFiles)
        self.__ui.pbDynamicExportFiles.clicked.connect(self.onDynamicExportFiles)

    def _dismantle(self):
        self.logger.Trace('ToolsSettingView.dismantle')

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageAssistiveTools)

    def onTabClicke(self):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageAssistiveTools)

    def onPackAddFiles(self):
        files, fileType = QFileDialog.getOpenFileNames(self.__ui.pageAssistiveTools, "Open File", "",
                                                       "All Files(*)")
        if files == []:
            return
        self.__model.packAddFiles(files)

    def onPackExportFiles(self):
        if self.__ui.lwPackList.count() == 0:
            return
        self.__model.packExportFiles(self.file_type)

    def onUnpackAddFiles(self):
        file, fileType = QFileDialog.getOpenFileName(self.__ui.pageAssistiveTools, "Open File", "",
                                                     "All Files(*)")
        if file == '':
            return
        self.__model.unpackAddFiles(file)

    def onUnpackExportFiles(self):
        if self.__ui.lwUnpackList.count() == 0:
            return
        self.__model.unpackExportFiles()

    def onDynamicAddFiles(self):
        file_list, file_type = QFileDialog.getOpenFileNames(self.__ui.pageAssistiveTools, "Open File", "",
                                                            "x2i (*.x2i);;xma (*.xma);;xsa(*xsa)")
        if file_list == []:
            return
        self.__model.dynamicAddFiles(file_list)

    def onDynamicExportFiles(self):
        if self.__ui.lwDynamicList.count() == 0:
            title = '_dynamic.json生成'
            info = '未选择文件...   '
            QMessageBox.information(self.__ui.pageAssistiveTools, title, info, QMessageBox.Ok, QMessageBox.Ok)
            return
        img_type = []
        if self.__ui.cbJpg.isChecked() or self.__ui.cbPng.isChecked():
            if self.__ui.cbJpg.isChecked():
                img_type.append('jpg')
            if self.__ui.cbPng.isChecked():
                img_type.append('png')
        else:
            title = '_dynamic.json生成'
            info = '请选择生成动态加载全景图的扩展名...   '
            QMessageBox.information(self.__ui.pageAssistiveTools, title, info, QMessageBox.Ok, QMessageBox.Ok)
            return
        self.__model.dynamicExportFiles(self.__ui.lwDynamicList, img_type)

    def handleUpdatePackList(self, _status, _data):
        for file_name in _status.pack_binary.keys():
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 25))
            item.setText(file_name)
            self.__ui.lwPackList.addItem(item)

    def handleUpdateUnpackList(self, _status, _data):
        for file_name in _status.unpack_binary.keys():
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 25))
            item.setText(file_name)
            self.__ui.lwUnpackList.addItem(item)

    def handleUpdateDynamicList(self, _status, _data):
        for file_name in _status.dynamic_binary.keys():
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 25))
            item.setText(file_name)
            self.__ui.lwDynamicList.addItem(item)

    def handleClean(self, _status, _data):
        if _status.clean_sign == 'pack':
            self.__ui.lwPackList.clear()
        if _status.clean_sign == 'unpack':
            self.__ui.lwUnpackList.clear()
        if _status.clean_sign == 'dynamic':
            self.__ui.lwDynamicList.clear()

    def buttonState(self, _radio):
        if _radio.isChecked():
            self.file_type = _radio.text()

    def handleMessage(self, _status, _data):
        title = _status.message["title"]
        info = _status.message["info"]
        QMessageBox.information(self.__ui.pageAssistiveTools, title, info, QMessageBox.Ok, QMessageBox.Ok)
