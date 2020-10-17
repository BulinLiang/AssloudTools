import tempfile
import PyMVCS
import PyArchive
from facade.app import AppFacade
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
from PyQt5.QtCore import Qt, QVariant, QFileInfo
from PyQt5.QtGui import QPixmap
from model.maker.RingPhotography360 import RingPhotography360MakerModel
from view.util import Util
import re


class RingPhotography360MakerView(PyMVCS.View):
    NAME = 'RingPhotography360MakerView'

    def _setup(self):
        self.logger.Trace('RingPhotography360MakerView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(RingPhotography360MakerModel.NAME)
        self.Route('/maker/RingPhotography360/update', self.handleUpdate)
        self.Route('/maker/RingPhotography360/file/activated', self.handleFileActivated)
        # 接收广播,清空ui
        self.Route('/maker/RingPhotography360/clean', self.handleClean)
        # 绑定事件
        self.__ui.rbRingPhotography360.toggled.connect(self.onTabToggle)
        self.__ui.pbRingPhotography360Add.clicked.connect(self.onAddClick)
        self.__ui.pbRingPhotography360Remove.clicked.connect(self.onRemoveClick)
        self.__ui.pbRingPhotography360Clean.clicked.connect(self.onCleanClick)
        self.__ui.pbRingPhotography360ExportWindows.clicked.connect(self.onExportWindowsClick)
        self.__ui.pbRingPhotography360ExportAndroid.clicked.connect(self.onExportAndroidClick)
        self.__ui.pbRingPhotography360Import.clicked.connect(self.onImportClick)
        self.__ui.lwRingPhotography360File.currentItemChanged.connect(self.onItemActivated)
        self.__ui.pbRingPhotography360Review.clicked.connect(self.onReviewClick)
        self.__ui.leRingPhotography360Title.textChanged.connect(self.onTitleChanged)
        self.__ui.pteRingPhotography360Description.textChanged.connect(self.onDescriptionChanged)

    def _dismantle(self):
        self.logger.Trace('RingPhotography360MakerView.dismantle')

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageRingPhotography360)

    def onAddClick(self):
        files, filter = QFileDialog.getOpenFileNames(self.__ui.pageRingPhotography360, "Open Images", "/",
                                                     "JPEG (*.jpg)")
        if files.count == 0:
            return
        self.__model.saveAddPhotos(files)

    def onTitleChanged(self, _value):
        self.__model.saveTitle(_value)

    def onDescriptionChanged(self):
        self.__model.saveDescription(self.__ui.pteRingPhotography360Description.toPlainText())

    def onImportClick(self):
        #
        file, filter = QFileDialog.getOpenFileName(self.__ui.pageRingPhotography360, "Open XSA Files", "/",
                                                   "XSA (*.xsa)")
        if file == "":
            return
        self.__model.saveImport(file)

    def onExportWindowsClick(self):
        file, filter = QFileDialog.getSaveFileName(self.__ui.pageRingPhotography360, "Save XSA Files", "/",
                                                   "XSA (*.xsa)")
        if file == "":
            return
        # TODO 文件名替换为xxx@windows.xsa
        file = re.match("(.*?)\.xsa$", str(file)).group(1) + "@windows.xsa"
        self.__model.saveExport(file)

    def onExportAndroidClick(self):
        file, filter = QFileDialog.getSaveFileName(self.__ui.pageRingPhotography360, "Save XSA Files", "/",
                                                   "XSA (*.xsa)")
        if file == "":
            return
        # TODO 文件名替换为xxx@android.xsa
        file = re.match("(.*?)\.xsa$", str(file)).group(1) + "@android.xsa"
        self.__model.saveExport(file)

    def onRemoveClick(self):
        pass

    def onCleanClick(self):
        # 交给数据层清除数据
        self.__model.clean()

    def onReviewClick(self):
        title = self.__ui.leRingPhotography360Title.text()
        description = self.__ui.pteRingPhotography360Description.toPlainText()
        img_list = self.__ui.lwRingPhotography360File.count()
        if img_list == 0:
            return
        # 列表有图片，没简介
        else:
            if title == '' or description == '':
                if title == '':
                    self.__ui.leRingPhotography360Title.setPlaceholderText("请输入标题")
                if description == '':
                    self.__ui.pteRingPhotography360Description.setPlaceholderText("请输入简介")
                return
            else:
                dir = tempfile.gettempdir()
                file = 'review@windows.xsa'
                self.__model.saveExport(dir + "/" + file)
                Util.review(dir + "/review.xsa")

    def onItemActivated(self, _item, _preitem):
        if _item == None:
            return
        self.__model.updateActivateFile(_item.text())

    def handleUpdate(self, _status, _data):
        for filename in _status.binary.keys():
            item = QListWidgetItem()
            item.setText(filename)
            self.__ui.lwRingPhotography360File.addItem(item)

    def handleFileActivated(self, _status, _data):
        pixmap = QPixmap()
        pixmap.loadFromData(_status.binary[_status.active])
        # print(_data)
        pixmap.scaled(self.__ui.lRingPhotography360Thumb.width(), self.__ui.lRingPhotography360Thumb.height())
        # 自适应大小
        self.__ui.lRingPhotography360Thumb.setScaledContents(True)
        # 给lRingPhotography360Thumb标签设置Pixmap
        self.__ui.lRingPhotography360Thumb.setPixmap(pixmap)

    # handle 处理clean事件
    def handleClean(self, _status, _data):
        self.__ui.leRingPhotography360Title.clear()
        self.__ui.pteRingPhotography360Description.clear()
        self.__ui.lwRingPhotography360File.clear()
