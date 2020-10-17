import PyMVCS
from facade.app import AppFacade
from model.product.MeeTouch import MeeTouchProductModel
from PyQt5.QtWidgets import QListWidgetItem, QCheckBox, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QSize


class MeeTouchProductView(PyMVCS.View):
    NAME = 'MeeTouchProductView'

    def _setup(self):
        self.logger.Trace('MeeTouchProductView.setup')
        self.__facade = PyMVCS.UIFacade.Find(AppFacade.NAME)
        self.__ui = self.__facade.ui
        self.__model = self.modelCenter.Find(MeeTouchProductModel.NAME)

        self.Route('/product/meetouch/projects/update', self.handleUpdateProjectsList)
        self.Route('/product/meetouch/check_path', self.handlePathCheck)
        self.Route('/product/meetouch/bundle/update', self.handleUpdateBundleList)
        self.Route('/product/meetouch/asset/update', self.handleUpdateAssetList)
        self.Route('/product/meetouch/assloud_link/update', self.handleUpdateAssloudLink)
        self.Route('/product/meetouch/message', self.handleMessage)

        # 是否是已经选择，并处于其他页面
        self.flag = 1
        # 先创建500个item存放assloud列表
        self.item_list = [None] * 1000

        "初始化MeeTouch"
        self.__ui.rbMeeTouch.clicked.connect(self.onTabClicke)
        self.__ui.rbMeeTouch.toggled.connect(self.onTabToggle)

        "选择项目"
        self.__ui.cbProjectList.currentIndexChanged.connect(self.onProjectActivated)

        "选择包"
        # self.bundleIsEdit = False
        self.__ui.lwLocalBundleList.currentItemChanged.connect(self.onBundleActivated)

        "编辑Catalog文件"
        self.__ui.pbEditCatalog.clicked.connect(self.onEditCatalog)

        "添加删除资源符号链接"
        self.__ui.pbAddLink.clicked.connect(self.onAddLink)
        self.__ui.pbClearLink.clicked.connect(self.onClearLink)

        "打包资源"
        self.__ui.pbExportToFolder.clicked.connect(self.onExportToFolder)
        "跳转到资源编辑界面"
        self.__ui.pbEditAsset.clicked.connect(self.onJumpAssetPage)
        "跳转到包编辑界面"
        self.__ui.pbEditBundle.clicked.connect(self.onJumpBundlePage)

        self.__ui.pbChecklog.setVisible(False)
        "运行"
        self.__ui.pbRUN.clicked.connect(self.onRUN)

    def _dismantle(self):
        self.logger.Trace('MeeTouchProductView.dismantle')

    def _initAssloudItems(self):
        for i in range(len(self.item_list)):
            box = QCheckBox()  # 实例化一个QCheckBox，吧文字传进去
            item = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QCheckBox
            item.setSizeHint(QSize(0, 25))
            self.item_list[i] = item
            self.__ui.lwAssloudList.addItem(item)  # 把QListWidgetItem加入QListWidget
            self.__ui.lwAssloudList.setItemWidget(item, box)  # 再把QCheckBox加入QListWidgetItem
            # 初始化隐藏item列表
            item.setHidden(True)

    def onTabClicke(self, _bool):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageMeeTouch)

    # 侧边栏标签开关
    def onTabToggle(self, _toggled):
        self.__ui.swPages.setCurrentWidget(self.__ui.pageMeeTouch)
        if self.flag:
            # 添加项目列表和资源列表
            self.addProjectsList()
            self.flag = 0

    def addProjectsList(self):
        self.__model.getProjectsList()

    def onProjectActivated(self, _index):
        self.__model.getBundleList(_index)

    def onBundleActivated(self, _item, _preitem):
        if _item == None:
            return
        self.__model.getAssetList(_item, Qt.UserRole)
        self.__model.getAssloudList(_item, Qt.UserRole)

    def onEditCatalog(self):
        self.__model.editCatalog()

    def onAddLink(self):
        # 如果bundle列表为空按钮不起作用
        if self.__ui.lwLocalBundleList.count() == 0:
            return
        self.__model.createLink(self.__ui.lwAssloudList, Qt.UserRole)

    def onClearLink(self):
        if self.__ui.lwLocalBundleList.count() == 0:
            return
        self.__model.clearLink(self.__ui.lwAssloudList)

    def onExportToFolder(self):
        if self.__ui.lwLocalBundleList.count() == 0:
            return
        fodler = QFileDialog.getExistingDirectory(self.__ui.pagePhotoAlbum, "Export Folder")
        if fodler == "":
            return
        self.__model.exportToFolder(self.__ui.cbProjectList.currentIndex(), fodler)

    def onJumpAssetPage(self):
        self.__ui.rbFiles.toggle()
        self.__ui.rbAssetEdit.toggle()
        self.__ui.swPages.setCurrentWidget(self.__ui.pageAssetEdit)

    def onJumpBundlePage(self):
        self.__ui.rbFiles.toggle()
        self.__ui.rbBundelEdit.toggle()
        self.__ui.swPages.setCurrentWidget(self.__ui.pageBundleEdit)

    def onRUN(self):
        if self.__ui.cbAppAddr.isChecked():
            self.__model.RUN(self.__ui.cbProjectList.currentIndex())
        else:
            return

    def handleUpdateProjectsList(self, _status, _data):
        # 初始化assloud资源列表，如果资源列表大于初始化设置的item_list值则自动加500
        while True:
            if len(_status.assloud_list) > len(self.item_list):
                self.item_list += [None] * (len(self.item_list) + 500)
            else:
                break
        self._initAssloudItems()
        self.__ui.cbProjectList.addItems(_status.alias_list)

    def handlePathCheck(self, _status, _data):
        index = self.__ui.cbProjectList.currentIndex()
        self.__ui.cbAppAddr.setText(_status.app_list[index])
        self.__ui.cbDataAddr.setText(_status.data_list[index])
        self.__ui.cbCatalogAddr.setText(_status.catalog_list[index])
        # 路径存在为1，不存在则为0
        self.__ui.cbAppAddr.setChecked(_status.check_flag[0])
        self.__ui.cbDataAddr.setChecked(_status.check_flag[1])
        self.__ui.cbCatalogAddr.setChecked(_status.check_flag[2])

    def handleUpdateBundleList(self, _status, _data):
        self.__ui.lwLocalBundleList.clear()
        self.__ui.lwLocalAssetList.clear()
        for k in _status.bundle_binary.keys():
            item = QListWidgetItem()
            item.setData(Qt.UserRole, k)
            item.setText(k)
            item.setSizeHint(QSize(0, 25))
            self.__ui.lwLocalBundleList.addItem(item)
        self.__ui.lwLocalBundleList.setCurrentRow(0)

    def handleUpdateAssetList(self, _status, _data):
        self.__ui.lwLocalAssetList.clear()
        # 只显示读取出来的文件夹列表(包括链接文件夹和非链接文件夹)
        asset_list = _status.bundle_binary[_status.active_bundle["item"]]["asset_dir"] + \
                     _status.bundle_binary[_status.active_bundle["item"]]["assets"]
        for asset in asset_list:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, asset)
            if len(asset.split("\\")) > 1:
                item.setText(asset.split("\\")[1])
            else:
                item.setText(asset)
            item.setSizeHint(QSize(0, 25))
            self.__ui.lwLocalAssetList.addItem(item)

    def handleUpdateAssloudLink(self, _status, _data):
        for i in range(len(_status.assloud_list)):
            assloud = _status.assloud_list[i]
            item = self.item_list[i]
            item.setHidden(False)
            checkbox = self.__ui.lwAssloudList.itemWidget(item)
            checkbox.setText(assloud)
            # 设置勾选了的复选框
            chose_list = _status.chose
            if assloud in chose_list:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

    def handleMessage(self, _status, _data):
        title = _status.message["title"]
        info = _status.message["info"]
        QMessageBox.information(self.__ui.pageAssetEdit, title, info, QMessageBox.Ok, QMessageBox.Ok)
