import tempfile
import PyMVCS
import PyArchive
from facade.app import AppFacade
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
from PyQt5.QtCore import Qt, QVariant, QFileInfo
from PyQt5.QtGui import QPixmap
from model.maker.Reciting import RecitingMakerModel
from view.util import Util
import re


class RecitingMakerView(PyMVCS.View):
    NAME = 'RecitingMakerView'

    def _setup(self):
        self.logger.Trace('RecitingMakerView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(RecitingMakerModel.NAME)
        self.Route('/maker/reciting/update', self.handleUpdate)
        # 绑定事件
        self.__ui.rbReciting.toggled.connect(self.onTabToggle)
        self.__ui.pbRecitingOpenAudio.clicked.connect(self.onAudioClick)
        self.__ui.pbRecitingExportWindows.clicked.connect(self.onExportWindowsClick)
        self.__ui.pbRecitingExportAndroid.clicked.connect(self.onExportAndroidClick)
        self.__ui.pbRecitingImport.clicked.connect(self.onImportClick)
        self.__ui.leRecitingTitle.textChanged.connect(self.onTitleChanged)
        self.__ui.leRecitingAuthor.textChanged.connect(self.onAuthorChanged)
        self.__ui.leRecitingReciter.textChanged.connect(self.onReciterChanged)
        self.__ui.pteRecitingContent.textChanged.connect(self.onContentChanged)
        self.__ui.pbRecitingReview.clicked.connect(self.onReviewClick)

    def _dismantle(self):
        self.logger.Trace('RecitingMakerView.dismantle')

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageReciting)

    def onAudioClick(self):
        file, filter = QFileDialog.getOpenFileName(self.__ui.pagePhotoAlbum, "Open Audio", "/", "Ogg (*.ogg)")
        if file == "":
            return
        self.__ui.leRecitingAudio.setText(QFileInfo(file).fileName())
        self.__model.saveAudio(file)

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
        file = re.match("(.*?)\.xsa$", str(file)).group(1) + "@android.xsa"
        self.__model.saveExport(file)

    def onRemoveClick(self):
        pass

    def onTitleChanged(self):
        self.__model.saveTitle(self.__ui.leRecitingTitle.text())

    def onAuthorChanged(self):
        self.__model.saveAuthor(self.__ui.leRecitingAuthor.text())

    def onReciterChanged(self):
        self.__model.saveReciter(self.__ui.leRecitingReciter.text())

    def onContentChanged(self):
        self.__model.saveContent(self.__ui.pteRecitingContent.toPlainText())

    def onReviewClick(self):
        dir = tempfile.gettempdir()
        file = 'review@windows.xsa'
        self.__model.saveExport(dir + "/" + file)
        Util.review(dir + "/review.xsa")

    def handleUpdate(self, _status, _data):
        pass
