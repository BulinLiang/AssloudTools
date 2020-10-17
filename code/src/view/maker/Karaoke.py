import tempfile
import PyMVCS
import PyArchive
from facade.app import AppFacade
from model.maker.Karaoke import KaraokeMakerModel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt, QVariant, QFileInfo
from PyQt5.QtGui import QPixmap
from view.util import Util
import re


class KaraokeMakerView(PyMVCS.View):
    NAME = 'KaraokeMakerView'

    def _setup(self):
        self.logger.Trace('KaraokeMakerView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(KaraokeMakerModel.NAME)
        self.Route('/maker/karaoke/update', self.handleUpdate)
        # 绑定事件
        self.__ui.rbKaraoke.toggled.connect(self.onTabToggle)
        self.__ui.pbKaraokeOpenMusic.clicked.connect(self.onMusicClick)
        self.__ui.pbKaraokeOpenAccompaniment.clicked.connect(self.onAccompanimentClick)
        self.__ui.pbKaraokeExportWindows.clicked.connect(self.onExportWindowsClick)
        self.__ui.pbKaraokeExportAndroid.clicked.connect(self.onExportAndroidClick)
        self.__ui.pbKaraokeImport.clicked.connect(self.onImportClick)
        self.__ui.pteKaraokeLyrics.textChanged.connect(self.onLyricsChanged)
        self.__ui.pbKaraokeReview.clicked.connect(self.onReviewClick)

    def _dismantle(self):
        self.logger.Trace('KaraokeMakerView.dismantle')

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageKaraoke)

    def onMusicClick(self):
        file, filter = QFileDialog.getOpenFileName(self.__ui.pagePhotoAlbum, "Open Audio", "/", "Ogg (*.ogg)")
        if file == "":
            return
        self.__ui.leKaraokeMusic.setText(QFileInfo(file).fileName())
        self.__model.saveMusic(file)

    def onAccompanimentClick(self):
        file, filter = QFileDialog.getOpenFileName(self.__ui.pagePhotoAlbum, "Open Audio", "/", "Ogg (*.ogg)")
        if file == "":
            return
        self.__ui.leKaraokeAccompaniment.setText(QFileInfo(file).fileName())
        self.__model.saveAccompaniment(file)

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

    def onLyricsChanged(self):
        self.__model.saveLyrics(self.__ui.pteKaraokeLyrics.toPlainText())

    def onReviewClick(self):
        dir = tempfile.gettempdir()
        file = 'review@windows.xsa'
        self.__model.saveExport(dir + "/" + file)
        Util.review(dir + "/review.xsa")

    def handleUpdate(self, _status, _data):
        pass
