import PyMVCS
import json
import os
from xpinyin import Pinyin
import re
import shutil


class BundleEditDocumentStatus(PyMVCS.Status):
    def __init__(self):
        super(BundleEditDocumentStatus, self).__init__()
        self.rootdir = ''
        self.bundle_dict = {}
        self.active_bundle = object
        # 活动bundle的信息和对应图片
        self.data = {}
        # xhub.cfg配置
        self.aliases = []
        self.apps = []
        self.datas = []
        self.catalogs = []
        self.labels = []
        self.message = ''
        # self.preloads = [{"type": "AudioClip", "name": "audio", "count": 2, "suffix": ".ogg"}]


class BundleEditDocumentModel(PyMVCS.Model):
    NAME = "BundleEditDocumentModel"

    def _setup(self):
        self.logger.Trace("BundleEditDocumentModel.setup")
        self.status = BundleEditDocumentStatus()

    def _dismantle(self):
        self.logger.Trace("BundleEditDocumentModel.dismantle")

    def getProjectList(self):
        home_path = os.path.expanduser('~')
        xhub_path = os.path.join(home_path, r'Documents\MeeX\xhub.cfg')
        if not os.path.exists(xhub_path):
            return
        f = open(xhub_path, 'r', encoding='utf8')
        xhub = json.loads(f.read())
        self.status.aliases = []
        self.status.apps = []
        self.status.datas = []
        self.status.catalogs = []
        self.status.labels = []
        for i in range(len(xhub['projects'])):
            self.status.aliases.append(xhub['projects'][i]['alias'])
            self.status.apps.append(xhub['projects'][i]['app'])
            self.status.datas.append(xhub['projects'][i]['data'])
            self.status.catalogs.append(xhub['projects'][i]['catalog'])
            self.status.labels.append(xhub['projects'][i]['label'])
        self.Broadcast("/document/bundle/projects/update", None)

    def getBundleDict(self, _index):
        self.status.bundle_dict = {}
        self.status.rootdir = self.status.datas[_index]
        try:
            self.catalog_path = os.path.join(self.status.datas[_index], self.status.catalogs[_index])
            bundle_list = os.listdir(os.path.join(self.status.rootdir, 'bundle'))
            if os.path.exists(self.catalog_path):
                with open(self.catalog_path, "r", encoding="UTF-8") as catalog_str:
                    # 添加新bundle时需要在配置文件中添加
                    self.catalog_list = json.loads(catalog_str.read())
                for catalog in self.catalog_list:
                    # 从配置文件中找目录中文名和文件名
                    zh_name = catalog["alias"]["zh_CN"].split('/')[0]
                    dir_name = catalog["bundle"]
                    if catalog["groups"] == ["catalog"] and catalog["bundle"] != '' and dir_name in bundle_list:
                        # {'标识':'_sign'} 使用实时读取
                        self.status.bundle_dict[zh_name] = dir_name
            else:
                self.status.bundle_dict = {}
            self.Broadcast("/document/bundle/item/update", None)
        except Exception as e:
            self.status.message = str(e)
            self.Broadcast("/document/bundle/message", None)

        # self.Broadcast("/document/asset/path_check", None)
        # self.Broadcast("/document/bundle/info/update", None)

    def updateInfo(self, _item, _uuid):
        self.status.active_bundle = _item
        name = _item.data(_uuid)
        uuid = self.status.bundle_dict[name]
        bunners = []
        bunner_name = Pinyin().get_initials(name, splitter='').lower()
        bunner_path = os.path.join(self.status.rootdir, 'banner/tech.meex.business')
        bunner_list = os.listdir(bunner_path)
        for bunner in bunner_list:
            if bunner.endswith('.png') and re.search(bunner_name, bunner.split('.')[0]):
                with open(os.path.join(bunner_path, bunner), 'rb') as img:
                    bunners.append(img.read())
        self.status.data['name'] = name
        self.status.data['uuid'] = uuid
        self.status.data['bunner'] = bunners
        self.Broadcast("/document/bundle/info/update", None)

    def openPath(self):
        path = os.path.join(self.status.rootdir, 'bundle')
        if os.path.exists(path):
            os.startfile(path)
        else:
            return

    # 添加item
    def addNewItem(self, _item, _uuid):
        bundle_name = _item.data(_uuid)
        bundle_dir = Pinyin().get_initials(_item.data(_uuid), splitter='').lower()
        self.status.active_bundle = _item
        if os.path.exists(
                os.path.join(self.status.rootdir, 'bundle', bundle_dir)):
            self.status.message = "文件夹已经存在"
            self.Broadcast('/document/bundle/message', None)
            return
        else:
            os.mkdir(os.path.join(self.status.rootdir, 'bundle', bundle_dir))
            self.addBundleToCatalog(_item, _uuid, bundle_name, bundle_dir)
            self.status.message = "添加资源成功"
            self.Broadcast('/document/bundle/message', None)
            self.Broadcast('/document/bundle/item/add', None)

    def deleteItem(self, _uuid):
        '''
         1、删除文件夹
         2、删除catalog_list中对应元素
         3、删除bundle_dict
         4、删除item
        '''
        bundle_name = self.status.active_bundle.data(_uuid)
        dir_name = self.status.bundle_dict[bundle_name]
        bundle_path = os.path.join(self.status.rootdir, 'bundle', dir_name)
        try:
            # 1、删除文件夹
            if os.path.exists(bundle_path):
                shutil.rmtree(bundle_path)
            # 遍历在新列表，删除在原列表
            for catalog in self.catalog_list[:]:
                if catalog["alias"]["zh_CN"].split('/')[0] == bundle_name:
                    # 2、删除catalog_list中对应元素，重新写入文件中
                    self.catalog_list.remove(catalog)
            with open(self.catalog_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(self.catalog_list, indent=4, ensure_ascii=False))
            # 3、删除bundle_dict
            self.status.bundle_dict.pop(bundle_name)
            # 4、删除item
            self.Broadcast('/document/bundle/item/delete', None)
            self.status.message = "删除包成功"
            self.Broadcast('/document/bundle/message', None)
        except Exception as e:
            self.status.message = str(e)
            self.Broadcast('/document/bundle/message', None)

    def saveExport(self, _item, _uuid, _name, _dir, _left, _right):
        self.addBundleToCatalog(_item, _uuid, _name, _dir)
        self.saveBunner(_left, _right, _name)
        self.status.message = "保存成功"
        self.Broadcast('/document/bundle/message', None)

    def addBundleToCatalog(self, _item, _uuid, _name, _dir):
        '''
        :param _item: 当前bundle列表中活动的item
        :param _name: item的新名字
        :param _id:   item的新id
        :param _uuid: Qt.UserRule
        1、重命名操作
            1.1、重命名文件夹
            1.2、更新catalog列表
            1.3、更新listItem列表
            1.4、重新设置_item.setData
        2、新增item
            2.1、新的bundle信息添加至catalog.json
            2.2、更新catalog_list
            2.3、添加新item信息到bundle_dict
            2.4、重新设置_item.setData
        '''
        old_name = _item.text()
        new_name = _name
        new_uuid = Pinyin().get_initials(new_name, splitter='').lower()
        new_dir = _dir
        if old_name in self.status.bundle_dict.keys():
            for i in range(len(self.catalog_list)):
                alias = self.catalog_list[i]['alias']['zh_CN']
                old_path = self.catalog_list[i]['path']
                if old_name == alias.split('/')[0]:
                    self.catalog_list[i]['alias']['zh_CN'] = new_name + '/' + alias.split("/")[1]
                    old_dir = self.catalog_list[i]['bundle']
                    if alias.split("/")[1] != '_':
                        self.catalog_list[i]['bundle'] = new_dir
                    self.catalog_list[i]['path'] = new_uuid + '/' + old_path.split("/")[1]
                    self.catalog_list[i]['uuid'] = new_uuid
                    if self.catalog_list[i]['bundle'] != '':
                        # 1、重命名文件夹
                        os.renames(os.path.join(self.status.rootdir, 'bundle', old_dir),
                                   os.path.join(self.status.rootdir, 'bundle', new_dir))
                    # 2、更新catalog列表
                    with open(self.catalog_path, 'w', encoding='utf-8') as f:
                        f.write(json.dumps(self.catalog_list, indent=4, ensure_ascii=False))
            # 3、更新listItem列表,并重新链接item.data
            self.status.bundle_dict.pop(old_name)
            self.status.bundle_dict[new_name] = new_dir
            _item.setData(_uuid, new_name)
            self.Broadcast('/document/bundle/item/rename', None)
        else:
            bundle_n = len(self.catalog_list)
            new_bundle_n = bundle_n // 2 + 1
            new_bundle = [
                {"alias": {"zh_CN": f"{new_name}/_"},
                 "bundle": "",
                 "id": new_bundle_n,
                 "index": new_bundle_n,
                 "path": f"{new_uuid}/_",
                 "tags": [],
                 "groups": ["catalog"],
                 "uuid": f"{new_uuid}"
                 },
                {"alias": {"zh_CN": f"{new_name}/default"},
                 "bundle": f"{new_dir}",
                 "id": 100 + new_bundle_n,
                 "index": 100 + new_bundle_n,
                 "path": f"{new_uuid}/default",
                 "tags": [],
                 "groups": ["catalog"],
                 "uuid": f"{new_uuid}/default"
                 }]
            # 1、新的bundle信息添加至catalog.json
            with open(self.catalog_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(self.catalog_list + new_bundle, indent=4, ensure_ascii=False))
            # 2、更新catalog_list
            with open(self.catalog_path, "r", encoding="UTF-8") as catalog_str:
                self.catalog_list = json.loads(catalog_str.read())
            # 3、添加新item信息到bundle_dict
            self.status.bundle_dict[new_name] = new_dir
            # 4、重新设置_item.setData
            _item.setData(_uuid, new_name)

    def saveBunner(self, _left, _right, _name):
        img_name = Pinyin().get_initials(_name, splitter='').lower()
        img_path = os.path.join(self.status.rootdir, 'banner/tech.meex.business')

        if _left != None and _right != None:
            _left.save(os.path.join(img_path, f'{img_name}@l.png'))
            _right.save(os.path.join(img_path, f'{img_name}@r.png'))

        elif _left != None and _right == None:
            _left.save(os.path.join(img_path, f'{img_name}.png'))

        elif _left == None and _right != None:
            _right.save(os.path.join(img_path, f'{img_name}.png'))