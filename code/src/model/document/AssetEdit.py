import PyMVCS
from PyQt5.QtCore import QFileInfo  # 获取文件信息，文件名，扩展名，路径等
import json
import os
import re
import shutil


class AssetEditDocumentStatus(PyMVCS.Status):
    def __init__(self):
        super(AssetEditDocumentStatus, self).__init__()
        self.rootdir = ''
        self.bundle_dict = {}
        self.asset_list = []
        self.active_asset = object
        self.active_bundle_text = ''
        self.active_asset_text = ''
        self.meta = {}
        self.alias_list = []
        self.app_list = []
        self.data_list = []
        self.catalog_list = []
        self.label_list = []
        # 检查完整性路径是否存在
        self.flag = [0, 0, 0]

        self.app_list = []
        # self.preloads = [{"type": "AudioClip", "name": "audio", "count": 2, "suffix": ".ogg"}]


class AssetEditDocumentModel(PyMVCS.Model):
    NAME = "AssetEditDocumentModel"

    def _setup(self):
        self.logger.Trace("AssetEditDocumentModel.setup")
        self.status = AssetEditDocumentStatus()

    def _dismantle(self):
        self.logger.Trace("AssetEditDocumentModel.dismantle")

    def getProjectList(self):
        home_path = os.path.expanduser('~')
        xhub_path = os.path.join(home_path, r'Documents\MeeX\xhub.cfg')
        if not os.path.exists(xhub_path):
            return
        f = open(xhub_path, 'r', encoding='utf8')
        xhub = json.loads(f.read())
        self.status.alias_list = []
        self.status.app_list = []
        self.status.data_list = []
        self.status.catalog_list = []
        self.status.label_list = []
        for i in range(len(xhub['projects'])):
            self.status.alias_list.append(xhub['projects'][i]['alias'])
            self.status.app_list.append(xhub['projects'][i]['app'])
            self.status.data_list.append(xhub['projects'][i]['data'])
            self.status.catalog_list.append(xhub['projects'][i]['catalog'])
            self.status.label_list.append(xhub['projects'][i]['label'])
        # print(self.status.alias_list, self.status.app_list, self.status.data_list)
        self.Broadcast("/document/asset/projects/update", None)

    def getBundlePath(self, _index):
        self.status.bundle_dict = {}
        if os.path.exists(self.status.data_list[_index]):
            self.status.rootdir = self.status.data_list[_index]
            self.status.flag[1] = 1
        else:
            self.status.flag[1] = 0
        # 配置文件路径
        project_path = os.path.join(self.status.data_list[_index], self.status.catalog_list[_index])
        if os.path.exists(project_path):
            self.status.flag[2] = 1
            catalog_str = open(project_path, "r", encoding="UTF-8")
            try:
                catalog_list = json.loads(catalog_str.read())
                catalog_str.close()
            except Exception as e:
                self.status.message = 'tech.meex.business.json文件格式有误： ' + str(e)
                self.Broadcast("/document/asset/message", None)
                return
            for catalog in catalog_list:
                # 从配置文件中找目录中文名和文件名
                if (catalog["groups"] == ["catalog"] or catalog["groups"] == []) and catalog["bundle"] != '':
                    # {'标识':'_sign'} 使用实时读取
                    self.status.bundle_dict[catalog["alias"]["zh_CN"].split('/')[0]] = catalog["bundle"]
        else:
            self.status.bundle_dict = {}
            self.status.asset_list = []
            self.status.flag[2] = 0

        self.Broadcast("/document/asset/bundlelist/update", None)
        # 选择项目后，项目资源路径错误时清空asset列表
        self.Broadcast("/document/asset/assetlist/update", None)

    def getAssetAppList(self):
        app_path = os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text, '_app')
        if os.path.exists(app_path):
            self.status.app_list = ['']
            file_list = os.listdir(app_path)
            for file in file_list:
                if file.endswith('xma'):
                    file_name = file.rsplit('.', 1)[0].split('@')[0] + '.' + file.rsplit('.', 1)[1]
                    self.status.app_list.append(file_name)
                    self.status.app_list = list(set(self.status.app_list))
            self.Broadcast("/document/asset/applist/update", None)
        else:
            os.makedirs(app_path)

    def updateAssetList(self, _item, _index):
        # 获取选中下拉列表item的文本
        key = _item.itemText(_index)
        self.status.active_bundle_text = self.status.bundle_dict[key]
        try:
            bundle_path = os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text)
            temp_list = os.listdir(bundle_path)
            self.status.asset_list = []
            for asset in temp_list:
                if not os.path.isfile(os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text,
                                                   asset)) and not re.search('_[a-z]', asset):
                    self.status.asset_list.append(asset)
            self.Broadcast("/document/asset/assetlist/update", None)
        except Exception as e:
            self.status.message = str(e)
            self.Broadcast('/document/asset/message', None)

    def getMeta(self, _item, _uuid):
        # self.logger.Trace(f'activate file: {_file}')
        self.status.active_asset_text = _item.data(_uuid)
        # 单击某个资源item后，取得meta.json路径
        meta_path = os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text,
                                 self.status.active_asset_text, "meta.json")
        img_path = os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text,
                                self.status.active_asset_text, "icon.png")
        self.status.meta[self.status.active_asset_text] = {"info": "", "icon": ""}
        # info存放meta.json
        if os.path.exists(meta_path):
            meta = open(meta_path, 'r', encoding="utf-8")
            self.status.meta[self.status.active_asset_text]["info"] = meta.read()
            meta.close()
        # icon存放icon.png
        if os.path.exists(img_path):
            img = open(img_path, 'rb')
            self.status.meta[self.status.active_asset_text]["icon"] = img.read()
            img.close()
        self.Broadcast('/document/asset/info/update', None)

    # 重命名item
    def renameItem(self, _item, _uuid):
        old_name = _item.data(_uuid)
        new_name = _item.text()
        if old_name == new_name:
            return
        self.status.active_asset = _item
        if os.path.exists(os.path.join(self.status.rootdir, self.status.active_bundle_text, new_name)):
            self.status.message = "文件已经存在"
            self.Broadcast('/document/asset/message', None)
            self.Broadcast('/document/asset/item/update', None)
            return
        os.rename(os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text, old_name),
                  os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text, new_name))
        _item.setData(_uuid, new_name)
        self.status.active_asset_text = new_name
        self.status.meta[self.status.active_asset_text] = {"icon": ""}
        self.status.message = "重命名资源成功"
        self.Broadcast('/document/asset/message', None)

    def openPath(self):
        asset_path = os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text)
        if os.path.exists(asset_path):
            os.startfile(asset_path)
        else:
            return

    # 添加item
    def addNewItem(self, _item, _uuid):
        if os.path.exists(
                os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text, _item.data(_uuid))):
            self.status.message = "文件夹已经存在"
            self.Broadcast('/document/asset/message', None)
            return
        else:
            os.mkdir(os.path.join(self.status.rootdir, 'bundle', self.status.active_bundle_text, _item.data(_uuid)))
            self.status.active_asset = _item
            self.status.message = "添加资源成功"
            self.Broadcast('/document/asset/message', None)
            self.Broadcast('/document/asset/item/add', None)

    # 删除item
    def deleteItem(self):
        asset_path = os.path.join(self.status.rootdir, 'bundle',
                                  self.status.active_bundle_text,
                                  self.status.active_asset_text)
        if os.path.exists(asset_path):
            # 软连接或文件夹
            if os.path.islink(asset_path):
                os.remove(asset_path)
            elif os.path.isdir(asset_path):
                shutil.rmtree(asset_path)
            else:
                return
            self.Broadcast('/document/asset/item/delete', None)
            self.status.message = "删除资源成功"
            self.Broadcast('/document/asset/message', None)
        elif not os.path.islink(asset_path):
            self.status.message = "删除失败，"
            self.Broadcast('/document/asset/message', None)
        else:
            return

    def saveIcon(self, _path):
        # icon存放icon.png
        copy_path = os.path.join(self.status.rootdir, 'bundle',
                                 self.status.active_bundle_text,
                                 self.status.active_asset_text,
                                 'icon.png')
        if os.path.exists(_path):
            # 读图片
            img = open(_path, 'rb')
            img_bytes = img.read()
            copy_img = open(copy_path, 'wb')
            self.status.meta[self.status.active_asset_text]["icon"] = img_bytes
            # 写图片
            copy_img.write(img_bytes)
            copy_img.close()
            img.close()
        self.Broadcast('/document/asset/icon/update', None)

    def saveExport(self, _file):
        savepath = os.path.join(self.status.rootdir, 'bundle',
                                self.status.active_bundle_text,
                                self.status.active_asset_text,
                                "meta.json")
        try:
            f = open(savepath, 'w', encoding="utf-8")
            f.write(json.dumps(_file, indent=4, ensure_ascii=False))
            f.close()
            self.status.message = "保存成功"
            self.Broadcast('/document/asset/message', None)
        except Exception as e:
            self.status.message = e
            self.Broadcast('/document/asset/message', None)
