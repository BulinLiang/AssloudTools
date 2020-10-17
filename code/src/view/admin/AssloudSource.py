# -*- coding: utf-8 -*-
"""
该文件完成功能：
    创建更改配置文件


    添加item和重命名item分开
"""

import PyMVCS
from facade.app import AppFacade
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QAbstractItemView, QLabel
from PyQt5.QtCore import Qt, QSize, QVariant, QFileInfo, pyqtSignal
from PyQt5.QtGui import QPixmap
from model.admin.AssloudSource import AssloudSourceAdminModel

import re
import json


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


class AssloudSourceAdminView(PyMVCS.View):
    NAME = 'AssloudSourceAdminView'

    def _setup(self):
        self.logger.Trace('AssloudSourceAdminView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(AssloudSourceAdminModel.NAME)

        # 创建Icon的Label
        self._createLabel()
        # 初始化控件
        self._initialization()

        self.Route('/assloud/bundle/update', self.handleBundleUpdate)
        self.Route('/assloud/asset/update', self.handleAssetUpdate)
        self.Route('/assloud/info/update', self.handleInfoUpdate)
        self.Route('/assloud/file/open', self.handleOpenExcel)
        self.Route('/assloud/item/add', self.handleAddItem)
        self.Route('/assloud/item/delete', self.handleDeleteItem)
        self.Route('/assloud/item/update', self.handleUpdateItem)
        self.Route('/assloud/icon/update', self.handleUpdateIcon)
        self.Route('/assloud/message', self.handleMessage)
        "选择资源整理菜单"
        self.__ui.rbAssloudSource.toggled.connect(self.onTabToggle)
        "打开Assloud路径"
        self.__ui.pbOpenAssloud.clicked.connect(self.onAddAssloudFolders)
        "Bundle包列表"
        self.bundleIsEdit = False
        # item发生变化
        self.__ui.lwBundleList.currentItemChanged.connect(self.onBundleActivated)
        # 双击编辑
        self.__ui.lwBundleList.itemDoubleClicked.connect(self.onBundleItemEditable)
        # 文本发生变化
        self.__ui.lwBundleList.itemChanged.connect(
            lambda: self.onItemRename(self.__ui.lwBundleList.item(self.__ui.lwBundleList.currentRow()), '_assloud'))
        # 当bundle中只剩下一个item时，currentItemChanged无法确认选中了那个item，并将bundleIsEdit设置成False，所以使用单击按钮
        self.__ui.lwBundleList.clicked.connect(self.onBundleClicked)
        # internalMove 内部拖动,drag 拖拽 drop 放下
        self.__ui.lwBundleList.setDragDropMode(QAbstractItemView.InternalMove)
        # 添加item
        self.__ui.pbBundleAdd.clicked.connect(lambda: self.onAddClicked('_assloud'))
        # 移除选中的Item
        self.__ui.pbBundleRemove.clicked.connect(lambda: self.onDeleteClicked('_assloud'))
        "Asset资源列表"
        self.assetIsEdit = False
        self.__ui.lwAssetList.currentItemChanged.connect(self.onAssetActivated)
        self.__ui.lwAssetList.itemDoubleClicked.connect(self.onAssetItemEditable)
        self.__ui.lwAssetList.itemChanged.connect(
            lambda: self.onItemRename(self.__ui.lwAssetList.item(self.__ui.lwAssetList.currentRow()), '_asset'))
        self.__ui.lwAssetList.clicked.connect(self.onAssetClicked)
        self.__ui.lwAssetList.setDragDropMode(QAbstractItemView.InternalMove)
        self.__ui.pbAssetAdd.clicked.connect(lambda: self.onAddClicked('_asset'))
        self.__ui.pbAssetRemove.clicked.connect(lambda: self.onDeleteClicked('_asset'))
        "保存照片"
        self.leIcon.dropDown[str].connect(self.ondropDown)
        "保存"
        self.__ui.pbSave.clicked.connect(self.onSaveClick)
        "index值发生改变"
        self.__ui.leIndex.textChanged.connect(self.onIndexTextChanged)
        "excel表插入"
        self.__ui.pbOpenExcel.clicked.connect(self.onOpenExcel)
        "excel 2 json  json 2 excel"
        self.__ui.pbGenerate.clicked.connect(self.onGenerateClick)

        self.__ui.pbAddXma.clicked.connect(self.onAddXma)
        self.__ui.pbAddPic.clicked.connect(self.onAddPic)

    # 功能不懂 ? ?
    def _dismantle(self):
        self.logger.Trace('AssloudSourceAdminView.dismantle')

    # 创建Icon显示框Label
    def _createLabel(self):
        self.leIcon = DropLabel(self.__ui.widget_19)  # DeopLabel重写Label事件，使其可以将桌面的图片拖动到Lable中进行Icon添加
        self.leIcon.setMinimumSize(QSize(125, 125))
        self.leIcon.setMaximumSize(QSize(125, 125))
        self.leIcon.setScaledContents(True)
        self.leIcon.setAlignment(Qt.AlignCenter)
        self.leIcon.setObjectName("leIcon")
        self.__ui.verticalLayout_29.addWidget(self.leIcon)

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageAssloudSource)

    # 所有控件初始化
    def _initialization(self):
        self.__ui.leIndex.setVisible(False)
        self.__ui.label_15.setVisible(False)
        self.__ui.leAssloudDir.setStyleSheet("color:black")
        self.__ui.leAssloudDir.clear()
        self.__ui.lwBundleList.clear()
        self.__ui.lwAssetList.clear()
        self.__ui.leExcelDir.clear()
        self.leIcon.clear()
        self.__ui.leIndex.clear()
        self.__ui.leTitle.clear()
        self.__ui.leCaption.clear()
        self.__ui.leLabel.clear()
        self.__ui.leTopic.clear()
        self.__ui.leAlias.clear()
        self.__ui.pteDescription.clear()
        self.__ui.cbImage2D.clearEditText()
        self.__ui.cbImage3D.clearEditText()
        self.__ui.cbVideo2D.clearEditText()
        self.__ui.cbVideo3D.clearEditText()
        self.__ui.cbApp.clearEditText()
        self.__ui.cbNative.clearEditText()
        self.__ui.cbBook.clearEditText()
        self.__ui.cbAudio.clearEditText()
        self.__ui.cbQrCode.clearEditText()
        self.__ui.lbMessage.clear()

    # 打开Assloud目录
    def onAddAssloudFolders(self):
        # 初始化所有控件
        self._initialization()
        # 获取文件路径
        _rootdir = QFileDialog.getExistingDirectory(self.__ui.pageAssloudSource, "Open File", "/")

        if _rootdir.endswith("/Assloud"):
            self.__model.addAssloudFolders(_rootdir)
        # 判断是否选择了文件\选择了是否是Assloud文件夹
        else:
            self.__ui.leAssloudDir.setStyleSheet("color:red")
            self.__ui.leAssloudDir.setText("请选择正确的Assloud路径...")
            return

    # 包列表的item发生改变，资源列表更新
    def onBundleActivated(self, _item, _preitem):
        self.__ui.lbMessage.clear()
        self.bundleIsEdit = False
        # 当item不为空的时候才设置
        if _item == None:
            return
        # 给保存json时，uri属性使用
        self.bundle_item = _item.text()
        self.__model.activeBundle(_item, Qt.UserRole)

    # 双击，将item变为可编辑状态
    # 必须加上 Qt.ItemIsDragEnabled | Qt.ItemIsSelectable 分别是 可移动 | 可选择
    def onBundleItemEditable(self, _item):
        _item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable)
        self.bundleIsEdit = True

    # 恢复可编辑状态
    def onBundleClicked(self, _index):
        self.bundleIsEdit = False

    # 添加item
    def onAddClicked(self, flag):
        if not self.__ui.leAssloudDir.text().endswith('bundle'):
            return
        new_item = QListWidgetItem()

        if flag == '_assloud':
            new_name = '新包名'
            new_item.setData(Qt.UserRole, new_name)
            new_item.setText(new_item.data(Qt.UserRole))
            self.__model.addNewItem(flag, new_item, Qt.UserRole)
        elif flag == '_asset':
            new_name = '新资源名'
            new_item.setData(Qt.UserRole, new_name)
            new_item.setText(new_item.data(Qt.UserRole))
            self.__model.addNewItem(flag, new_item, Qt.UserRole)

    # 删除item
    def onDeleteClicked(self, flag):
        if flag == '_assloud':
            # 包列表为空
            if self.__ui.lwBundleList.count() == 0:
                return
            # 没有选择item
            if self.__ui.lwBundleList.currentRow() != -1:
                # 是否处在编辑状态
                if not self.bundleIsEdit:
                    self.__model.deleteItem(flag)
                else:
                    self.__ui.lbMessage.setText('编辑状态，无法删除')
            else:
                self.__ui.lbMessage.setText('请选择需要修改的包！')
                return
        elif flag == '_asset':
            if self.__ui.lwBundleList.count() == 0 and self.__ui.lwAssetList.count() == 0:
                return
            if self.__ui.lwAssetList.currentRow() != -1:
                if not self.bundleIsEdit:
                    self.__model.deleteItem(flag)
                else:
                    self.__ui.lbMessage.setText('编辑状态，无法删除')
            else:
                self.__ui.lbMessage.setText('请选择需要修改的资源！')
                return

    # 当item文本发生变化，更改BundleItem名
    def onItemRename(self, _item, flag):
        if flag == '_assloud':
            # 当item没有任何文字时恢复原来的文本
            if _item.text() == '' or re.search('[\\\*?"<>|/]', _item.text()):
                _item.setText(_item.data(Qt.UserRole))
                self.__ui.lbMessage.setText('文件名不能包含以下字符:\ / * ? " < > |')
                return

            self.__model.renameItem('_assloud', _item, Qt.UserRole)
        elif flag == '_asset':
            if _item.text() == '' or re.search('[\\\*?"<>|/]', _item.text()):
                _item.setText(_item.data(Qt.UserRole))
                self.__ui.lbMessage.setText('文件名不能包含以下字符:\ / * ? " < > |')
                return
            self.__model.renameItem('_asset', _item, Qt.UserRole)

    # 资源列表的item发生改变，信息更新
    def onAssetActivated(self, _item, _preitem):
        self.__ui.lbMessage.clear()
        if _item == None:
            return
        # 获取信息
        self.__model.getMeta(_item, Qt.UserRole)

    # 将item变为可编辑状态
    def onAssetItemEditable(self, _item):
        _item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable)
        self.assetIsEdit = True

    def onAssetClicked(self, _index):
        self.assetIsEdit = False

    def ondropDown(self, _path):
        if self.__ui.lwAssetList.currentRow() == -1:
            return
        if _path.endswith('.png'):
            self.__model.saveIcon(_path)
        else:
            self.__ui.lbMessage.setText('图片必须为png格式')

    # 将ui控件数据保存到json
    def onSaveClick(self):
        if self.__ui.lwAssetList.count() == 0:
            return
        self.__ui.lbMessage.clear()

        file = {}
        language = self.__ui.cbLanguage.currentText()
        index = self.__ui.leIndex.text()
        alias = self.__ui.leAlias.text()
        title = self.__ui.leTitle.text()
        caption = self.__ui.leCaption.text()
        label = self.__ui.leLabel.text()
        topic = self.__ui.leTopic.text()
        description = self.__ui.pteDescription.toPlainText()
        image2D = self.__ui.cbImage2D.currentText()
        image3D = self.__ui.cbImage3D.currentText()
        video2D = self.__ui.cbVideo2D.currentText()
        video3D = self.__ui.cbVideo3D.currentText()
        model = self.__ui.cbModel.currentText()
        app = self.__ui.cbApp.currentText()
        native = self.__ui.cbNative.currentText()
        book = self.__ui.cbBook.currentText()
        audio = self.__ui.cbAudio.currentText()
        qrCode = self.__ui.cbQrCode.currentText()

        index = self._isNumber(index)
        if index == -1:
            return

        file["index"] = index
        file["uri"] = self.bundle_item + '/' + title

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
            self.__ui.leIndex.setText(self.__ui.leIndex.text() + "(请输入数字)")
            self.__ui.leIndex.setStyleSheet("color:red")
            self.__ui.leIndex.setFocus()
            return -1

    # 当index控件数据发生改变时，改变数据样式
    def onIndexTextChanged(self):
        self.__ui.leIndex.setStyleSheet("color:black")

    # 打开excel
    def onOpenExcel(self):
        self.__ui.lbMessage.clear()
        self.__ui.leExcelDir.clear()
        # 获取文件路径
        _exceldir, filter = QFileDialog.getOpenFileName(self.__ui.pagePhotoAlbum, "Open Audio", "/",
                                                        "xlsx File(*.xlsx);;xls File (*.xls)")
        # 判断是否选择了文件
        if _exceldir == '':
            return

        self.__model.openExcel(_exceldir)

    # excel生成json
    def onGenerateClick(self):
        self.__ui.lbMessage.clear()
        if self.__ui.leExcelDir.text() == '':
            return

        flag = self.__ui.cbExhange.currentText()
        # 生成meta.jdon
        self.__model.Generate(flag)

    def onAddXma(self):
        self.__model.moveXma(self.__ui.leAssloudDir.text())

    def onAddPic(self):
        if self.__ui.lwAssetList.currentRow() == -1:
            self.__ui.lbMessage.setText("请选择资源")
        else:
            self.__model.addPic(self.__ui.leAssloudDir.text())

    def handleBundleUpdate(self, _status, _data):
        self.__ui.lwBundleList.clear()
        self.__ui.leAssloudDir.setText(_status.rootdir)
        for bundle_name in _status.bundle:
            # 包列表
            item_bundle = QListWidgetItem()
            item_bundle.setData(Qt.UserRole, bundle_name)  # 使用setData给items添加对应的uuid，之后控制方便
            item_bundle.setText(item_bundle.data(Qt.UserRole))
            self.__ui.lwBundleList.addItem(item_bundle)

    def handleAssetUpdate(self, _status, _data):
        self.__ui.lwAssetList.clear()
        for asset_name in _status.asset:
            item_asset = QListWidgetItem()  # 资源列表
            item_asset.setData(Qt.UserRole, asset_name)  # 设置item的uid
            item_asset.setText(item_asset.data(Qt.UserRole))
            self.__ui.lwAssetList.addItem(item_asset)

    def handleInfoUpdate(self, _status, _data):
        self.__ui.lbMessage.clear()
        # _status.active 监听按下那个item，信息跟随改变
        data = _status.meta[_status.active_asset_text]
        try:
            # 有图有信息
            if data["icon"] != "" and data["info"] != "":
                pixmap = QPixmap()
                pixmap.loadFromData(data["icon"])
                self.leIcon.setScaledContents(True)  # 自适应大小
                self.leIcon.setPixmap(pixmap)
                info = json.loads(data["info"])
                if "index" in info.keys():
                    self.__ui.leIndex.setText(str(info["index"]))
                else:
                    self.__ui.leIndex.setText("")
                for k in info['title'].keys():
                    if k == "en_US":
                        self.__ui.cbLanguage.setCurrentIndex(0)
                        self.__ui.leTitle.setText(info["title"]["en_US"])
                        self.__ui.leCaption.setText(info["caption"]["en_US"])
                        self.__ui.leLabel.setText(info["label"]["en_US"])
                        self.__ui.leTopic.setText(info["topic"]["en_US"])
                        self.__ui.leAlias.setText(info["alias"]["en_US"])
                        self.__ui.pteDescription.setPlainText(info["description"]["en_US"])
                    if k == "zh_CN":
                        self.__ui.cbLanguage.setCurrentIndex(1)
                        self.__ui.leTitle.setText(info["title"]["zh_CN"])
                        self.__ui.leCaption.setText(info["caption"]["zh_CN"])
                        self.__ui.leLabel.setText(info["label"]["zh_CN"])
                        self.__ui.leTopic.setText(info["topic"]["zh_CN"])
                        self.__ui.leAlias.setText(info["alias"]["zh_CN"])
                        self.__ui.pteDescription.setPlainText(info["description"]["zh_CN"])
                self.__ui.cbImage2D.lineEdit().setText(info["image2D"])
                self.__ui.cbImage3D.lineEdit().setText(info["image3D"])
                self.__ui.cbVideo2D.lineEdit().setText(info["video2D"])
                self.__ui.cbVideo3D.lineEdit().setText(info["video3D"])
                self.__ui.cbModel.lineEdit().setText(info["model"])
                self.__ui.cbApp.lineEdit().setText(info["app"])
                self.__ui.cbNative.lineEdit().setText(info["native"])
                self.__ui.cbBook.lineEdit().setText(info["book"])
                self.__ui.cbAudio.lineEdit().setText(info["audio"])
                self.__ui.cbQrCode.lineEdit().setText(info["qrCode"])

            # 有图无信息
            elif data["icon"] != "" and data["info"] == "":
                pixmap = QPixmap()
                pixmap.loadFromData(data["icon"])
                self.leIcon.setPixmap(pixmap)
                self.__ui.leIndex.clear()
                self.__ui.leTitle.clear()
                self.__ui.leCaption.clear()
                self.__ui.leLabel.clear()
                self.__ui.leTopic.clear()
                self.__ui.leAlias.clear()
                self.__ui.pteDescription.clear()
                self.__ui.cbImage2D.clearEditText()
                self.__ui.cbImage3D.clearEditText()
                self.__ui.cbVideo2D.clearEditText()
                self.__ui.cbVideo3D.clearEditText()
                self.__ui.cbApp.clearEditText()
                self.__ui.cbNative.clearEditText()
                self.__ui.cbBook.clearEditText()
                self.__ui.cbAudio.clearEditText()
                self.__ui.cbQrCode.clearEditText()
            # 无图有信息
            elif data["icon"] == "" and data["info"] != "":
                self.leIcon.clear()
                info = json.loads(data["info"])
                if "index" in info.keys():
                    self.__ui.leIndex.setText(str(info["index"]))
                else:
                    self.__ui.leIndex.setText("")
                for k in info['title'].keys():
                    if k == "en_US":
                        self.__ui.cbLanguage.setCurrentIndex(0)
                        self.__ui.leTitle.setText(info["title"]["en_US"])
                        self.__ui.leCaption.setText(info["caption"]["en_US"])
                        self.__ui.leLabel.setText(info["label"]["en_US"])
                        self.__ui.leTopic.setText(info["topic"]["en_US"])
                        self.__ui.leAlias.setText(info["alias"]["en_US"])
                        self.__ui.pteDescription.setPlainText(info["description"]["en_US"])
                    if k == "zh_CN":
                        self.__ui.cbLanguage.setCurrentIndex(1)
                        self.__ui.leTitle.setText(info["title"]["zh_CN"])
                        self.__ui.leCaption.setText(info["caption"]["zh_CN"])
                        self.__ui.leLabel.setText(info["label"]["zh_CN"])
                        self.__ui.leTopic.setText(info["topic"]["zh_CN"])
                        self.__ui.leAlias.setText(info["alias"]["zh_CN"])
                        self.__ui.pteDescription.setPlainText(info["description"]["zh_CN"])
                self.__ui.cbImage2D.lineEdit().setText(info["image2D"])
                self.__ui.cbImage3D.lineEdit().setText(info["image3D"])
                self.__ui.cbVideo2D.lineEdit().setText(info["video2D"])
                self.__ui.cbVideo3D.lineEdit().setText(info["video3D"])
                self.__ui.cbApp.lineEdit().setText(info["app"])
                self.__ui.cbNative.lineEdit().setText(info["native"])
                self.__ui.cbBook.lineEdit().setText(info["book"])
                self.__ui.cbAudio.lineEdit().setText(info["audio"])
                self.__ui.cbQrCode.lineEdit().setText(info["qrCode"])
            # 无图无信息
            else:
                self.leIcon.clear()
                self.__ui.leIndex.clear()
                self.__ui.leTitle.clear()
                self.__ui.leCaption.clear()
                self.__ui.leLabel.clear()
                self.__ui.leTopic.clear()
                self.__ui.leAlias.clear()
                self.__ui.pteDescription.clear()
                self.__ui.cbImage2D.clearEditText()
                self.__ui.cbImage3D.clearEditText()
                self.__ui.cbVideo2D.clearEditText()
                self.__ui.cbVideo3D.clearEditText()
                self.__ui.cbApp.clearEditText()
                self.__ui.cbNative.clearEditText()
                self.__ui.cbBook.clearEditText()
                self.__ui.cbAudio.clearEditText()
                self.__ui.cbQrCode.clearEditText()
        except Exception as e:
            self.__ui.lbMessage.setText(str(e))

    def handleAddItem(self, _status, _flag):
        if _flag == '_assloud':
            self.__ui.lwBundleList.insertItem(0, _status.active_bundle)
        elif _flag == '_asset':
            self.__ui.lwAssetList.insertItem(0, _status.active_asset)

    def handleDeleteItem(self, _status, _flag):
        if _flag == '_assloud':
            self.__ui.lwBundleList.takeItem(self.__ui.lwBundleList.currentRow())
        elif _flag == '_asset':
            self.__ui.lwAssetList.takeItem(self.__ui.lwAssetList.currentRow())

    def handleUpdateItem(self, _status, _flag):
        if _flag == '_assloud':
            _status.active_bundle.setText(_status.active_bundle_text)
        elif _flag == '_asset':
            _status.active_asset.setText(_status.active_asset_text)

    def handleUpdateIcon(self, _status, _flag):
        pixmap = QPixmap()
        pixmap.loadFromData(_status.meta[_status.active_asset_text]["icon"])
        self.leIcon.setScaledContents(True)  # 自适应大小
        self.leIcon.setPixmap(pixmap)

    def handleOpenExcel(self, _status, _data):
        self.__ui.leExcelDir.setStyleSheet("color:black")
        self.__ui.leExcelDir.setText(_status.exceldir)

    def handleMessage(self, _status, _data):
        self.__ui.lbMessage.setText(_status.message)

