import PyMVCS
from facade.app import AppFacade
from model.document.BundleEdit import BundleEditDocumentModel
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QAbstractItemView
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap
import json
import re


# 重写Label控件
class DropLabel(QLabel):
    # 设置自定义信号函数pyqtSignal在使用时默认传递一个参数
    dropDown = pyqtSignal(object, str)

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
        # 图片是放在DropLabel对象内，并不是Qlabel对象
        self.dropDown.emit(self, image_path)
        event.acceptProposedAction()


class BundleEditDocumentView(PyMVCS.View):
    NAME = 'BundleEditDocumentView'

    def _setup(self):
        self.logger.Trace('BundleEditDocumentView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(BundleEditDocumentModel.NAME)

        # 创建Icon的Label
        self._createLabel()

        self.Route('/document/bundle/projects/update', self.handleUpdateProjectsList)
        self.Route('/document/bundle/item/update', self.handleUpdateBundleList)
        self.Route('/document/bundle/info/update', self.handleUpdateInfo)
        self.Route('/document/bundle/item/add', self.handleAddItem)
        self.Route('/document/bundle/item/rename', self.handleRenameItem)
        self.Route('/document/bundle/item/delete', self.handleDeleteItem)
        self.Route('/document/bundle/message', self.handleMessage)

        "初始化MeeTouch"
        self.__ui.rbBundelEdit.clicked.connect(self.onTabClicked)
        self.__ui.rbBundelEdit.toggled.connect(self.onTabToggle)
        "选择项目"
        self.__ui.cbBundleProjectList.currentIndexChanged.connect(self.onProjectActivated)
        "选择包"
        self.__ui.lwBundleEditList.currentItemChanged.connect(self.onBundleActivated)
        "打开路径"
        self.__ui.pbBundleOpenPath.clicked.connect(self.onOpenPath)
        "保存照片"
        self.banner1.dropDown.connect(self.ondropDown)
        self.banner2.dropDown.connect(self.ondropDown)
        "添加"
        self.__ui.pbBundleEditAdd.clicked.connect(self.onAddClicked)
        "删除"
        self.__ui.pbBundleEditRemove.clicked.connect(self.onDeleteClicked)
        "保存"
        self.__ui.pbBundleSave.clicked.connect(self.onSaveClick)
        "返回"
        self.__ui.pbBundleBack.clicked.connect(self.onComeBack)

    def _dismantle(self):
        self.logger.Trace('BundleEditDocumentView.dismantle')

    def onTabClicked(self, _bool):
        if _bool:
            self.__ui.swPages.setCurrentWidget(self.__ui.pageBundleEdit)

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        if not _toggled:
            self._initialization()
        self._addProjectList()

    # 创建Icon显示框Label
    def _createLabel(self):
        self.banner1 = DropLabel(self.__ui.wBanner1)
        self.banner1.setScaledContents(True)
        self.banner1.setAlignment(Qt.AlignCenter)
        self.banner1.setObjectName("banner1")
        self.banner2 = DropLabel(self.__ui.wBanner2)
        self.banner2.setScaledContents(True)
        self.banner2.setAlignment(Qt.AlignCenter)
        self.banner2.setObjectName("banner2")
        self.__ui.verticalLayout_47.addWidget(self.banner1)
        self.__ui.verticalLayout_48.addWidget(self.banner2)

    def _initialization(self):
        self.__ui.lwBundleEditList.clear()
        self.__ui.lbFolderName.clear()
        self.__ui.lbFolderUuid.clear()
        self.banner1.clear()
        self.banner2.clear()
        self.__ui.lbBundleMessage.clear()

    def _addProjectList(self):
        self.__model.getProjectList()

    def onProjectActivated(self, _index):
        self._initialization()
        if self.__ui.cbBundleProjectList.count() == 0:
            return
        self.__model.getBundleDict(_index)

    def onBundleActivated(self, _item, _preitem):
        if self.__ui.lwBundleEditList.count() == 0 or _item == None:
            return
        self.__model.updateInfo(_item, Qt.UserRole)

    def onBundleItemEditable(self, _item):
        _item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable)
        self.BundleIsEdit = True

    def onOpenPath(self):
        if self.__ui.lwBundleEditList.count() == 0:
            return
        self.__model.openPath()

    def onAddClicked(self):
        if self.__ui.lwBundleEditList.count() == 0:
            return
        new_name = '新包名'
        new_item = QListWidgetItem()
        new_item.setData(Qt.UserRole, new_name)
        new_item.setText(new_name)
        new_item.setSizeHint(QSize(0, 25))
        self.__model.addNewItem(new_item, Qt.UserRole)

    # 删除item
    def onDeleteClicked(self):
        if self.__ui.lwBundleEditList.count() == 0:
            return
        if self.__ui.lwBundleEditList.currentRow() != -1:
            self.__model.deleteItem(Qt.UserRole)
        else:
            self.__ui.lbBundleMessage.setText('请选择需要修改的资源！')
            return

    def ondropDown(self, _label, _path):
        if self.__ui.lwBundleEditList.currentRow() == -1:
            return
        if _path.endswith('.png'):
            pixmap = QPixmap(_path)
            _label.setScaledContents(True)  # 自适应大小
            _label.setPixmap(pixmap)
        else:
            self.__ui.lbBundleMessage.setText('图片必须为png格式')

    def onSaveClick(self):
        # 没选中item
        if self.__ui.lwBundleEditList.currentRow() == -1:
            return
        item = self.__ui.lwBundleEditList.selectedItems()[0]
        bundle_dir = self.__ui.lbFolderUuid.text()
        new_name = self.__ui.lbFolderName.text()
        left = self.banner1.pixmap()
        right = self.banner2.pixmap()
        self.__model.saveExport(item, Qt.UserRole, new_name, bundle_dir, left, right)

    def onComeBack(self):
        self.__ui.rbBundelEdit.setChecked(False)
        self.__ui.rbFiles.setChecked(False)
        self.__ui.rbTerminal.toggle()
        self.__ui.rbMeeTouch.toggle()
        self.__ui.swPages.setCurrentWidget(self.__ui.pageMeeTouch)

    def handleUpdateProjectsList(self, _status, _data):
        self.__ui.cbBundleProjectList.clear()
        self.__ui.cbBundleProjectList.addItems(_status.aliases)

    def handleUpdateBundleList(self, _status, _data):
        self.__ui.lwBundleEditList.clear()
        for bundle in _status.bundle_dict.keys():
            item = QListWidgetItem()
            item.setData(Qt.UserRole, bundle)
            item.setText(bundle)
            item.setSizeHint(QSize(0, 25))
            self.__ui.lwBundleEditList.addItem(item)
        self.__ui.lwBundleEditList.setCurrentRow(0)

    def handleUpdateInfo(self, _status, _data):
        self.__ui.lbBundleMessage.clear()
        self.__ui.lbFolderName.clear()
        self.__ui.lbFolderUuid.clear()
        self.banner1.clear()
        self.banner2.clear()
        self.__ui.lbFolderUuid.setText(_status.data['uuid'])
        self.__ui.lbFolderName.setText(_status.data['name'])

        for i in range(len(_status.data["bunner"])):
            if i == 0:
                pixmap1 = QPixmap()
                pixmap1.loadFromData(_status.data["bunner"][0])
                self.banner1.setScaledContents(True)  # 自适应大小
                self.banner1.setPixmap(pixmap1)
            if i == 1:
                pixmap2 = QPixmap()
                pixmap2.loadFromData(_status.data["bunner"][1])
                self.banner2.setScaledContents(True)  # 自适应大小
                self.banner2.setPixmap(pixmap2)

    def handleAddItem(self, _status, _data):
        _status.active_bundle.setSizeHint(QSize(0, 25))
        self.__ui.lwBundleEditList.insertItem(0, _status.active_bundle)
        self.__ui.lwBundleEditList.setCurrentRow(0)

    def handleRenameItem(self, _status, _data):
        _status.active_bundle.setText(self.__ui.lbFolderName.text())

    def handleDeleteItem(self, _status, _data):
        self.__ui.lwBundleEditList.takeItem(self.__ui.lwBundleEditList.currentRow())

    def handleMessage(self, _status, _data):
        self.__ui.lbBundleMessage.setText(_status.message)
