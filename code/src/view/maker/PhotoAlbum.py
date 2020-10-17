import tempfile
import PyMVCS
import PyArchive
from facade.app import AppFacade
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QApplication
from PyQt5.QtGui import QPixmap
from model.maker.PhotoAlbum import PhotoAlbumMakerModel
from view.util import Util
import re


class PhotoAlbumMakerView(PyMVCS.View):
    NAME = 'PhotoAlbumMakerView'

    def _setup(self):
        self.logger.Trace('PhotoAlbumMakerView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(PhotoAlbumMakerModel.NAME)
        self.Route('/maker/photoalbum/update', self.handleUpdate)
        self.Route('/maker/photoalbum/file/activated', self.handleFileActivated)
        # 接收广播,清空ui
        self.Route('/maker/photoalbum/clean', self.handleClean)
        # 绑定事件
        self.__ui.rbPhotoAlbum.toggled.connect(self.onTabToggle)
        self.__ui.pbPhotoAlbumAdd.clicked.connect(self.onAddClick)
        self.__ui.pbPhotoAlbumRemove.clicked.connect(self.onRemoveClick)
        self.__ui.pbPhotoAlbumClean.clicked.connect(self.onCleanClick)
        self.__ui.pbPhotoAlbumExportWindows.clicked.connect(self.onExportWindowsClick)
        self.__ui.pbPhotoAlbumExportAndroid.clicked.connect(self.onExportAndroidClick)
        self.__ui.pbPhotoAlbumImport.clicked.connect(self.onImportClick)
        # currentItemChanged 选中的item发生了改变
        # currentItemChanged 信号返回的有两个指针所以函数需要接受两个参数
        self.__ui.lwPhotoAlbumFile.currentItemChanged.connect(self.onItemActivated)
        self.__ui.ptePhotoAlbumText.textChanged.connect(self.onTextChanged)
        self.__ui.pbPhotoAlbumReview.clicked.connect(self.onReviewClick)
        '''
            当单击相册目录时获取屏幕分辨率
        '''
        self.__ui.rbPhotoAlbum.clicked.connect(self.onGetResolution)

    def _dismantle(self):
        self.logger.Trace('PhotoAlbumMakerView.dismantle')

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        self.__ui.swPages.setCurrentWidget(self.__ui.pagePhotoAlbum)

    def onAddClick(self):
        files, filter = QFileDialog.getOpenFileNames(self.__ui.pagePhotoAlbum, "Open Images", "/", "JPEG (*.jpg)")
        if files.count == 0:
            return
        self.__model.saveAddPhotos(files)

    def onImportClick(self):
        file, filter = QFileDialog.getOpenFileName(self.__ui.pagePhotoAlbum, "Open XSA Files", "/", "XSA (*.xsa)")
        if file == "":
            return
        self.__model.saveImport(file)

    def onExportWindowsClick(self):
        file, filter = QFileDialog.getSaveFileName(self.__ui.pagePhotoAlbum, "Save XSA Files", "/", "XSA (*.xsa)")
        if file == "":
            return
        # TODO 文件名替换为xxx@windows.xsa
        file = re.match("(.*?)\.xsa$", str(file)).group(1) + "@windows.xsa"
        self.__model.saveExport(file)

    def onExportAndroidClick(self):
        file, filter = QFileDialog.getSaveFileName(self.__ui.pagePhotoAlbum, "Save XSA Files", "/", "XSA (*.xsa)")

        if file == "":
            return
        # TODO 文件名替换为xxx@android.xsa
        file = re.match("(.*?)\.xsa$", file).group(1) + "@android.xsa"
        self.__model.saveExport(file)

    def onRemoveClick(self):
        pass

    def onCleanClick(self):
        # 交给数据层清除数据
        self.__model.clean()

    def onReviewClick(self):
        dir = tempfile.gettempdir()
        file = 'review@windows.xsa'
        self.__model.saveExport(dir + "/" + file)
        Util.review(dir + "/review.xsa")

    def onTextChanged(self):
        self.__model.saveText(self.__ui.ptePhotoAlbumText.toPlainText())

    # 当进行清空操作时需要判断当前item指针是否为空
    # 指针判断 None，非''
    def onItemActivated(self, _item, _preitem):
        if _item == None:
            return
        self.__model.updateActivateFile(_item.text())

    # ----待定功能----
    def onGetResolution(self):
        # 获取屏幕分辨率
        self.desktop = QApplication.desktop()

        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        print(self.width, self.height)

    def handleUpdate(self, _status, _data):
        for filename in _status.photos.keys():
            item = QListWidgetItem()
            item.setText(filename)
            self.__ui.lwPhotoAlbumFile.addItem(item)

    def handleFileActivated(self, _status, _data):
        self.__ui.ptePhotoAlbumText.setEnabled(True)
        pixmap = QPixmap()
        pixmap.loadFromData(_status.binary[_status.active])
        self.__ui.lPhotoAlbumThumb.setPixmap(pixmap)
        self.__ui.ptePhotoAlbumText.setPlainText(_status.photos[_status.active])

    # handle 处理clean事件
    def handleClean(self, _status, _data):
        self.__ui.lwPhotoAlbumFile.clear()
        self.__ui.lPhotoAlbumThumb.clear()
        self.__ui.ptePhotoAlbumText.clear()
        self.__ui.ptePhotoAlbumText.setEnabled(False)
        self.__ui.ptePhotoAlbumText.setPlainText("请选择照片")
