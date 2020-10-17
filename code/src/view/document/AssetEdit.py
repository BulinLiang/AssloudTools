import PyMVCS
from facade.app import AppFacade
from model.document.AssetEdit import AssetEditDocumentModel
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QAbstractItemView, QMessageBox
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap
import json
import re


# TODO MeeTouch跳转该界面如何加载资源 -->文件夹路径

# 重写Label控件
class DropLabel(QLabel):
    # 设置自定义信号函数pyqtSignal在使用时默认传递一个参数
    dropDown = pyqtSignal([str])

    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # 一定要使用super，因为程序先看子类方法再去看父类方法,子类方法覆盖了
        # 父类方法,会到导致dropEvent()的其他方法无法使用
        # event:事件对象
        super(DropLabel, self).dropEvent(event)
        image = event.mimeData().text()
        image_path = re.sub('^file:///', '', image)
        self.dropDown[str].emit(image_path)
        event.acceptProposedAction()


class AssetEditDocumentView(PyMVCS.View):
    NAME = 'AssetEditDocumentView'

    def _setup(self):
        self.logger.Trace('AssetEditDocumentView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(AssetEditDocumentModel.NAME)

        # 创建Icon的Label
        self._createLabel()
        # 初始化控件
        self._initialization()

        self.Route('/document/asset/projects/update', self.handleUpdateProjectsList)
        # self.Route('/document/asset/path_check', self.handlePathCheck)
        self.Route('/document/asset/bundlelist/update', self.handleUpdateBundleList)
        self.Route('/document/asset/assetlist/update', self.handleUpdateAssetList)

        self.Route('/document/asset/applist/update', self.handleAddApp)

        self.Route('/document/asset/icon/update', self.handleUpdateIcon)
        self.Route('/document/asset/info/update', self.handleUpdateInfo)
        self.Route('/document/asset/item/add', self.handleAddItem)
        self.Route('/document/asset/item/delete', self.handleDeleteItem)
        self.Route('/document/asset/message', self.handleMessage)

        "初始化MeeTouch"
        self.__ui.rbAssetEdit.clicked.connect(self.onTabClicked)
        self.__ui.rbAssetEdit.toggled.connect(self.onTabToggle)
        self.__ui.pbAssetRefresh.clicked.connect(self.onTabToggle)
        "选择项目"
        self.__ui.cbAssetProjectList.currentIndexChanged.connect(self.onProjectActivated)
        "选择包"
        self.__ui.cbAssetBundleList.currentIndexChanged.connect(self.onBundleActivated)
        "选择资源"
        self.AssetIsEdit = False
        self.__ui.lwAssetEditList.currentItemChanged.connect(self.onAssetActivated)
        # 双击编辑
        self.__ui.lwAssetEditList.itemDoubleClicked.connect(self.onAssetItemEditable)
        # 文本发生变化
        self.__ui.lwAssetEditList.itemChanged.connect(
            lambda: self.onItemRename(self.__ui.lwAssetEditList.item(self.__ui.lwAssetEditList.currentRow())))
        # 单击item其他位置确认更改的item名字
        self.__ui.lwAssetEditList.clicked.connect(self.onAssetClicked)
        # internalMove 内部拖动,drag 拖拽 drop 放下
        self.__ui.lwAssetEditList.setDragDropMode(QAbstractItemView.InternalMove)
        "保存照片"
        self.leAssetIcon.dropDown[str].connect(self.ondropDown)
        "打开路径"
        self.__ui.pbAssetOpenPath.clicked.connect(self.onOpenPath)
        "添加"
        self.__ui.pbAssetEditAdd.clicked.connect(self.onAddClicked)
        "删除"
        self.__ui.pbAssetEditRemove.clicked.connect(self.onDeleteClicked)
        "保存"
        self.__ui.pbAssetSave.clicked.connect(self.onSaveClick)
        self.__ui.leAssetIndex.textChanged.connect(self.onIndexTextChanged)
        "返回"
        self.__ui.pbAssetBack.clicked.connect(self.onComeBack)

    def _dismantle(self):
        self.logger.Trace('AssetEditDocumentView.dismantle')

    # 侧边栏标签开关
    def onTabClicked(self, _bool):
        if _bool:
            self.__ui.swPages.setCurrentWidget(self.__ui.pageAssetEdit)

    def onTabToggle(self, _toggle):
        if not _toggle:
            self._initialization()
        self.__ui.swPages.setCurrentWidget(self.__ui.pageAssetEdit)
        self._addProjectList()
        self._getAssetAppList()

    # 创建Icon显示框Label
    def _createLabel(self):
        self.leAssetIcon = DropLabel(self.__ui.wIcon)  # DeopLabel重写Label事件，使其可以将桌面的图片拖动到Lable中进行Icon添加
        self.leAssetIcon.setMinimumSize(QSize(125, 125))
        self.leAssetIcon.setMaximumSize(QSize(125, 125))
        self.leAssetIcon.setScaledContents(True)
        self.leAssetIcon.setAlignment(Qt.AlignCenter)
        self.leAssetIcon.setObjectName("leAssetIcon")
        self.__ui.verticalLayout_37.addWidget(self.leAssetIcon)

    def _initialization(self):
        self.__ui.cbAssetBundleList.clear()
        self.__ui.lwAssetEditList.clear()
        self.leAssetIcon.clear()
        self.__ui.leAssetIndex.clear()
        self.__ui.leAssetTitle.clear()
        self.__ui.leAssetCaption.clear()
        self.__ui.leAssetLabel.clear()
        self.__ui.leAssetTopic.clear()
        self.__ui.leAssetAlias.clear()
        self.__ui.pteAssetDescription.clear()
        self.__ui.cbAssetImage2D.clearEditText()
        self.__ui.cbAssetImage3D.clearEditText()
        self.__ui.cbAssetVideo2D.clearEditText()
        self.__ui.cbAssetVideo3D.clearEditText()
        self.__ui.cbAssetApp.clearEditText()
        self.__ui.cbAssetNative.clearEditText()
        self.__ui.cbAssetBook.clearEditText()
        self.__ui.cbAssetAudio.clearEditText()
        self.__ui.cbAssetQrCode.clearEditText()

    def _getAssetAppList(self):
        if self.__ui.cbAssetBundleList.count() == 0:
            return
        self.__model.getAssetAppList()

    def _addProjectList(self):
        self.__model.getProjectList()

    def onProjectActivated(self, _index):
        self._initialization()
        if self.__ui.cbAssetProjectList.count() == 0:
            return
        self.__model.getBundlePath(_index)

    def onBundleActivated(self, _index):
        # 当item不为空的时候才设置
        if self.__ui.cbAssetBundleList.count() == 0:
            return
        self.__model.updateAssetList(self.__ui.cbAssetBundleList, _index)

    def onAssetActivated(self, _item, _preitem):
        if _item == None:
            return
        # 获取信息
        self.__model.getMeta(_item, Qt.UserRole)

    def onAssetItemEditable(self, _item):
        _item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable)
        self.AssetIsEdit = True

    # 当item文本发生变化，更改BundleItem名
    def onItemRename(self, _item):
        # 当item没有任何文字时恢复原来的文本
        if _item.text() == '' or re.search('[\\\*?"<>|/]', _item.text()):
            _item.setText(_item.data(Qt.UserRole))
            QMessageBox.information(self.__ui.pageAssetEdit, 'information', '文件名不能包含以下字符:\ / * ? " < > |',
                                    QMessageBox.Ok, QMessageBox.Ok)
            return
        self.__model.renameItem(_item, Qt.UserRole)

    # 恢复可编辑状态
    def onAssetClicked(self, _index):
        self.AssetIsEdit = False

    def onOpenPath(self):
        if self.__ui.cbAssetBundleList.count() == 0:
            return
        self.__model.openPath()

    def onAddClicked(self):
        if self.__ui.cbAssetBundleList.count() == 0:
            return
        new_item = QListWidgetItem()
        new_name = '新资源名'
        new_item.setData(Qt.UserRole, new_name)
        new_item.setText(new_item.data(Qt.UserRole))
        self.__model.addNewItem(new_item, Qt.UserRole)

    # 删除item
    def onDeleteClicked(self):
        if self.__ui.cbAssetBundleList.count() == 0 and self.__ui.lwAssetEditList.count() == 0:
            return
        if self.__ui.lwAssetEditList.currentRow() != -1:

            if not self.AssetIsEdit:
                res = QMessageBox.information(self.__ui.pageAssetEdit, 'information', '是否删除？',
                                              QMessageBox.Ok | QMessageBox.No,
                                              QMessageBox.No)
                if res == QMessageBox.Ok:
                    self.__model.deleteItem()
            else:
                QMessageBox.information(self.__ui.pageAssetEdit, 'information', '编辑状态，无法删除！', QMessageBox.Ok,
                                        QMessageBox.Ok)
        else:
            QMessageBox.information(self.__ui.pageAssetEdit, 'information', '请选择需要修改的资源！', QMessageBox.Ok,
                                    QMessageBox.Ok)
            return

    def ondropDown(self, _path):
        if self.__ui.lwAssetEditList.currentRow() == -1:
            return
        if _path.endswith('.png'):
            self.__model.saveIcon(_path)
        else:
            QMessageBox.information(self.__ui.pageAssetEdit, 'information', '图片必须为png格式！', QMessageBox.Ok,
                                    QMessageBox.Ok)

    def onSaveClick(self):
        if self.__ui.lwAssetEditList.count() == 0:
            return
        self.__ui.lbAssetMessage.clear()

        file = {}
        language = self.__ui.cbAssetLanguage.currentText()
        index = self.__ui.leAssetIndex.text()
        alias = self.__ui.leAssetAlias.text()
        title = self.__ui.leAssetTitle.text()
        caption = self.__ui.leAssetCaption.text()
        label = self.__ui.leAssetLabel.text()
        topic = self.__ui.leAssetTopic.text()
        description = self.__ui.pteAssetDescription.toPlainText()
        image2D = self.__ui.cbAssetImage2D.currentText()
        image3D = self.__ui.cbAssetImage3D.currentText()
        video2D = self.__ui.cbAssetVideo2D.currentText()
        video3D = self.__ui.cbAssetVideo3D.currentText()
        model = self.__ui.cbAssetModel.currentText()
        app = self.__ui.cbAssetApp.currentText()
        native = self.__ui.cbAssetNative.currentText()
        book = self.__ui.cbAssetBook.currentText()
        audio = self.__ui.cbAssetAudio.currentText()
        qrCode = self.__ui.cbAssetQrCode.currentText()

        index = self._isNumber(index)
        if index == -1:
            return

        file["index"] = index
        file["uri"] = self.__ui.cbAssetBundleList.currentText() + '/' + title

        file["alias"] = {language: alias}
        file["title"] = {language: title}
        file["caption"] = {language: caption}
        file["label"] = {language: label}
        file["topic"] = {language: topic}
        file["description"] = {language: description}
        file["image2D"] = image2D
        file["image3D"] = image3D
        file["video2D"] = video2D
        file["video3D"] = video3D
        file["model"] = model
        file["app"] = app
        file["native"] = native
        file["audio"] = audio
        file["book"] = book
        file["qrCode"] = qrCode
        self.__model.saveExport(file)

    def _isNumber(self, _num):
        if _num == '':
            return 0
        elif re.search("[0-9]+$", _num):
            return int(_num)
        elif re.search("[^0-9]", _num):
            self.__ui.leAssetIndex.setText(self.__ui.leAssetIndex.text() + "(请输入数字)")
            self.__ui.leAssetIndex.setStyleSheet("color:red")
            self.__ui.leAssetIndex.setFocus()
            return -1

    def onIndexTextChanged(self):
        self.__ui.leAssetIndex.setStyleSheet("color:black")

    def onComeBack(self):
        self.__ui.rbTerminal.toggle()
        self.__ui.rbMeeTouch.toggle()
        self.__ui.rbMeeTouch.setChecked(True)
        if self.__ui.rbMeeTouch.isChecked():
            self.__ui.swPages.setCurrentWidget(self.__ui.pageMeeTouch)

    def handleUpdateProjectsList(self, _status, _data):
        self.__ui.cbAssetProjectList.clear()
        self.__ui.cbAssetProjectList.addItems(_status.alias_list)

    def handleUpdateBundleList(self, _status, _data):
        self.__ui.cbAssetBundleList.clear()
        self.__ui.cbAssetBundleList.addItems(_status.bundle_dict.keys())

    def handleUpdateAssetList(self, _status, _data):
        self.__ui.lwAssetEditList.clear()
        for asset in _status.asset_list:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, asset)
            item.setText(asset)
            item.setSizeHint(QSize(0, 25))
            self.__ui.lwAssetEditList.addItem(item)
        self.__ui.lwAssetEditList.setCurrentRow(0)

    def handleAddApp(self, _status, _data):
        self.__ui.cbAssetApp.clear()
        self.__ui.cbAssetApp.addItems(_status.app_list)

    def handleUpdateIcon(self, _status, _data):
        pixmap = QPixmap()
        pixmap.loadFromData(_status.meta[_status.active_asset_text]["icon"])
        self.leAssetIcon.setScaledContents(True)  # 自适应大小
        self.leAssetIcon.setPixmap(pixmap)

    def handleUpdateInfo(self, _status, _data):
        self.__ui.lbAssetMessage.clear()
        data = _status.meta[_status.active_asset_text]
        try:
            # 有图有信息
            if data["icon"] != "" and data["info"] != "":
                pixmap = QPixmap()
                pixmap.loadFromData(data["icon"])
                self.leAssetIcon.setScaledContents(True)  # 自适应大小
                self.leAssetIcon.setPixmap(pixmap)
                info = json.loads(data["info"])
                if "index" in info.keys():
                    self.__ui.leAssetIndex.setText(str(info["index"]))
                else:
                    self.__ui.leAssetIndex.setText("")
                for k in info['title'].keys():
                    if k == "en_US":
                        self.__ui.cbAssetLanguage.setCurrentIndex(0)
                        self.__ui.leAssetTitle.setText(info["title"]["en_US"])
                        self.__ui.leAssetCaption.setText(info["caption"]["en_US"])
                        self.__ui.leAssetLabel.setText(info["label"]["en_US"])
                        self.__ui.leAssetTopic.setText(info["topic"]["en_US"])
                        self.__ui.leAssetAlias.setText(info["alias"]["en_US"])
                        self.__ui.pteAssetDescription.setPlainText(info["description"]["en_US"])
                    if k == "zh_CN":
                        self.__ui.cbAssetLanguage.setCurrentIndex(1)
                        self.__ui.leAssetTitle.setText(info["title"]["zh_CN"])
                        self.__ui.leAssetCaption.setText(info["caption"]["zh_CN"])
                        self.__ui.leAssetLabel.setText(info["label"]["zh_CN"])
                        self.__ui.leAssetTopic.setText(info["topic"]["zh_CN"])
                        self.__ui.leAssetAlias.setText(info["alias"]["zh_CN"])
                        self.__ui.pteAssetDescription.setPlainText(info["description"]["zh_CN"])
                self.__ui.cbAssetImage2D.lineEdit().setText(info["image2D"])
                self.__ui.cbAssetImage3D.lineEdit().setText(info["image3D"])
                self.__ui.cbAssetVideo2D.lineEdit().setText(info["video2D"])
                self.__ui.cbAssetVideo3D.lineEdit().setText(info["video3D"])
                self.__ui.cbAssetModel.lineEdit().setText(info["model"])
                self.__ui.cbAssetApp.lineEdit().setText(info["app"])
                self.__ui.cbAssetNative.lineEdit().setText(info["native"])
                self.__ui.cbAssetBook.lineEdit().setText(info["book"])
                self.__ui.cbAssetAudio.lineEdit().setText(info["audio"])
                self.__ui.cbAssetQrCode.lineEdit().setText(info["qrCode"])

            # 有图无信息
            elif data["icon"] != "" and data["info"] == "":
                pixmap = QPixmap()
                pixmap.loadFromData(data["icon"])
                self.leAssetIcon.setPixmap(pixmap)
                self.__ui.leIndex.clear()
                self.__ui.leAssetTitle.clear()
                self.__ui.leAssetCaption.clear()
                self.__ui.leAssetLabel.clear()
                self.__ui.leAssetTopic.clear()
                self.__ui.leAssetAlias.clear()
                self.__ui.pteAssetDescription.clear()
                self.__ui.cbAssetImage2D.clearEditText()
                self.__ui.cbAssetImage3D.clearEditText()
                self.__ui.cbAssetVideo2D.clearEditText()
                self.__ui.cbAssetVideo3D.clearEditText()
                self.__ui.cbAssetApp.clearEditText()
                self.__ui.cbAssetNative.clearEditText()
                self.__ui.cbAssetBook.clearEditText()
                self.__ui.cbAssetAudio.clearEditText()
                self.__ui.cbAssetQrCode.clearEditText()
            # 无图有信息
            elif data["icon"] == "" and data["info"] != "":
                self.leAssetIcon.clear()
                info = json.loads(data["info"])
                if "index" in info.keys():
                    self.__ui.leIndex.setText(str(info["index"]))
                else:
                    self.__ui.leIndex.setText("")
                for k in info['title'].keys():
                    if k == "en_US":
                        self.__ui.cbAssetLanguage.setCurrentIndex(0)
                        self.__ui.leAssetTitle.setText(info["title"]["en_US"])
                        self.__ui.leAssetCaption.setText(info["caption"]["en_US"])
                        self.__ui.leAssetLabel.setText(info["label"]["en_US"])
                        self.__ui.leAssetTopic.setText(info["topic"]["en_US"])
                        self.__ui.leAssetAlias.setText(info["alias"]["en_US"])
                        self.__ui.pteAssetDescription.setPlainText(info["description"]["en_US"])
                    if k == "zh_CN":
                        self.__ui.cbAssetLanguage.setCurrentIndex(1)
                        self.__ui.leAssetTitle.setText(info["title"]["zh_CN"])
                        self.__ui.leAssetCaption.setText(info["caption"]["zh_CN"])
                        self.__ui.leAssetLabel.setText(info["label"]["zh_CN"])
                        self.__ui.leAssetTopic.setText(info["topic"]["zh_CN"])
                        self.__ui.leAssetAlias.setText(info["alias"]["zh_CN"])
                        self.__ui.pteAssetDescription.setPlainText(info["description"]["zh_CN"])
                self.__ui.cbAssetImage2D.lineEdit().setText(info["image2D"])
                self.__ui.cbAssetImage3D.lineEdit().setText(info["image3D"])
                self.__ui.cbAssetVideo2D.lineEdit().setText(info["video2D"])
                self.__ui.cbAssetVideo3D.lineEdit().setText(info["video3D"])
                self.__ui.cbAssetApp.lineEdit().setText(info["app"])
                self.__ui.cbAssetNative.lineEdit().setText(info["native"])
                self.__ui.cbAssetBook.lineEdit().setText(info["book"])
                self.__ui.cbAssetAudio.lineEdit().setText(info["audio"])
                self.__ui.cbAssetQrCode.lineEdit().setText(info["qrCode"])
            # 无图无信息
            else:
                self.leAssetIcon.clear()
                self.__ui.leIndex.clear()
                self.__ui.leAssetTitle.clear()
                self.__ui.leAssetCaption.clear()
                self.__ui.leAssetLabel.clear()
                self.__ui.leAssetTopic.clear()
                self.__ui.leAssetAlias.clear()
                self.__ui.pteAssetDescription.clear()
                self.__ui.cbAssetImage2D.clearEditText()
                self.__ui.cbAssetImage3D.clearEditText()
                self.__ui.cbAssetVideo2D.clearEditText()
                self.__ui.cbAssetVideo3D.clearEditText()
                self.__ui.cbAssetApp.clearEditText()
                self.__ui.cbAssetNative.clearEditText()
                self.__ui.cbAssetBook.clearEditText()
                self.__ui.cbAssetAudio.clearEditText()
                self.__ui.cbAssetQrCode.clearEditText()
        except Exception as e:
            self.__ui.lbAssetMessage.setText(str(e))

    def handleAddItem(self, _status, _data):
        _status.active_asset.setSizeHint(QSize(0, 25))
        self.__ui.lwAssetEditList.insertItem(0, _status.active_asset)

    def handleDeleteItem(self, _status, _data):
        self.__ui.lwAssetEditList.takeItem(self.__ui.lwAssetEditList.currentRow())

    def handleMessage(self, _status, _data):
        QMessageBox.information(self.__ui.pageAssetEdit, 'information', _status.message, QMessageBox.Ok,
                                QMessageBox.Ok)
