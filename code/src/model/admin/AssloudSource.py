'''
-*- coding: utf-8 -*-

    该文件完成功能：
        数据交换
'''
import json
import PyMVCS
from PyQt5.QtCore import QFileInfo
from model.util import Util
import os, shutil
import xlrd
import re
from xpinyin import Pinyin


# 数据初始化
class AssloudSourceAdminStatus(PyMVCS.Status):
    def __init__(self):
        super(AssloudSourceAdminStatus, self).__init__()
        self.rootdir = ''
        self.exceldir = ''
        # class列表
        self.bundle = []
        self.asset = []
        # 活动class item，因为是使用uuid提取文本数据，如果只使用object类型的话，
        # 在同时判断acitve_bundle和active_asset时也会使用到uuid，这时就会冲突如函数activeAssset
        self.active_bundle = object
        self.active_asset = object
        self.active_bundle_text = ''
        self.active_asset_text = ''
        self.meta = {}
        self.message = ''
        self.preloads = [{'type': 'Folder', 'name': 'folder', 'count': 2, 'suffix': ''}]


class AssloudSourceAdminModel(PyMVCS.Model):
    NAME = 'AssloudSourceAdminModel'

    def _setup(self):
        self.logger.Trace('AssloudSourceAdminModel.setup')
        self.status = AssloudSourceAdminStatus()

    def _dismantle(self):
        self.logger.Trace('AssloudSourceAdminModel.dismantle')

    def clean(self):
        self.status.bundle = []
        self.Broadcast('/assloud/clean', None)

    def addAssloudFolders(self, _path):
        self.status.bundle = []
        self.status.rootdir = os.path.join(re.sub('/', '\\\\', _path), "bundle")
        try:
            _files = os.listdir(os.path.join(self.status.rootdir))
            for file in _files:
                # 获取文件名
                filename = QFileInfo(file).fileName()
                # 忽略已存在的
                if filename in self.status.bundle:
                    continue
                self.status.bundle.append(filename)
            # 更新ui，更新包列表
            self.Broadcast('/assloud/bundle/update', None)
        except:
            self.status.message = 'Assloud文件夹下没有bundle文件夹'
            self.Broadcast('/assloud/message', None)

    def activeBundle(self, _item, _uuid):  # _uuid存放item的UserRole
        # 监听包文件名
        # self.logger.Trace(f'activate file: {_file}')
        self.status.asset = []
        self.status.active_bundle_text = _item.data(_uuid)

        asset_path = os.path.join(self.status.rootdir, self.status.active_bundle_text)
        if not os.path.exists(asset_path):
            self.status.message = "没有该目录,可能被删除"
            self.Broadcast('/assloud/message', None)
            return
        asset_list = os.listdir(asset_path)
        for asset_name in asset_list:
            isdir = os.path.isdir(os.path.join(asset_path, asset_name))
            if isdir and not re.match("_[a-z]+$", asset_name):
                self.status.asset.append(asset_name)

        self.Broadcast('/assloud/asset/update', None)

    # 获取info
    def getMeta(self, _item, _uuid):
        # self.logger.Trace(f'activate file: {_file}')
        self.status.active_asset_text = _item.data(_uuid)
        self.status.active_asset = _item
        # 单击某个资源item后，取得meta.json路径
        meta_path = os.path.join(self.status.rootdir, self.status.active_bundle_text, self.status.active_asset_text,
                                 "meta.json")
        img_path = os.path.join(self.status.rootdir, self.status.active_bundle_text, self.status.active_asset_text,
                                "icon.png")
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

        self.Broadcast('/assloud/info/update', None)

    # 添加item
    def addNewItem(self, _flag, _item, _uuid):
        if _flag == '_assloud':
            # 当文件已经存在时
            if os.path.exists(os.path.join(self.status.rootdir, _item.data(_uuid))):
                self.status.message = "文件夹已经存在"
                self.Broadcast('/assloud/message', None)
                return
            else:
                os.mkdir(os.path.join(self.status.rootdir, _item.data(_uuid)))
                self.status.active_bundle = _item
                self.status.message = "添加包成功"
                self.Broadcast('/assloud/message', None)
                self.Broadcast('/assloud/item/add', _flag)
        elif _flag == '_asset':
            if os.path.exists(os.path.join(self.status.rootdir, self.status.active_bundle_text, _item.data(_uuid))):
                self.status.message = "文件夹已经存在"
                self.Broadcast('/assloud/message', None)
                return
            else:
                os.mkdir(os.path.join(self.status.rootdir, self.status.active_bundle_text, _item.data(_uuid)))
                self.status.active_asset = _item
                self.status.message = "添加资源成功"
                self.Broadcast('/assloud/message', None)
                self.Broadcast('/assloud/item/add', _flag)

    # 删除item
    def deleteItem(self, _flag):
        bundle_path = os.path.join(self.status.rootdir, self.status.active_bundle_text)
        asset_path = os.path.join(self.status.rootdir, self.status.active_bundle_text, self.status.active_asset_text)
        if _flag == '_assloud':
            # if os.listdir(os.path.join(self.status.rootdir, self.status.active_bundle_text)) != []:
            # 删除非空文件夹
            if os.path.exists(bundle_path):
                shutil.rmtree(bundle_path)
                self.Broadcast('/assloud/item/delete', _flag)
                self.status.message = "删除包成功"
                self.Broadcast('/assloud/message', None)
            else:
                return
        elif _flag == '_asset':
            if os.path.exists(asset_path):
                shutil.rmtree(asset_path)
                self.Broadcast('/assloud/item/delete', _flag)
                self.status.message = "删除资源成功"
                self.Broadcast('/assloud/message', None)
            else:
                return

    # 重命名item
    def renameItem(self, _flag, _item, _uuid):
        old_name = _item.data(_uuid)
        new_name = _item.text()

        if _flag == '_assloud':
            if old_name == new_name:
                return

            # 获取活动的item
            self.status.active_bundle = _item
            if os.path.exists(os.path.join(self.status.rootdir, old_name)):
                # 当文件存在时不做任何操作
                if os.path.exists(os.path.join(self.status.rootdir, new_name)):
                    self.status.message = "文件已经存在"
                    self.Broadcast('/assloud/message', None)
                    self.Broadcast('/assloud/item/update', _flag)
                    return
            else:
                self.status.message = "没有该目录,可能被删除"
                self.Broadcast('/assloud/message', None)
                return

            os.rename(os.path.join(self.status.rootdir, old_name),
                      os.path.join(self.status.rootdir, new_name))
            # 重命名后_uuid要与新文件名重新建立连接
            _item.setData(_uuid, new_name)
            # 如果不加上的话，在重命名后活动的item新名字不会改变
            self.status.active_bundle_text = new_name
            self.status.message = "重命名包成功"
            self.Broadcast('/assloud/message', None)

        elif _flag == '_asset':
            if old_name == new_name:
                return
            self.status.active_asset = _item
            if os.path.exists(os.path.join(self.status.rootdir, self.status.active_bundle_text, new_name)):
                self.status.message = "文件已经存在"
                self.Broadcast('/assloud/message', None)
                self.Broadcast('/assloud/item/update', _flag)
                return
            os.rename(os.path.join(self.status.rootdir, self.status.active_bundle_text, old_name),
                      os.path.join(self.status.rootdir, self.status.active_bundle_text, new_name))
            _item.setData(_uuid, new_name)
            self.status.active_asset_text = new_name
            self.status.meta[self.status.active_asset_text] = {"icon": ""}
            self.status.message = "重命名资源成功"
            self.Broadcast('/assloud/message', None)

    def saveIcon(self, _path):
        # icon存放icon.png
        copy_path = os.path.join(self.status.rootdir, self.status.active_bundle_text, self.status.active_asset_text,
                                 'icon.png')
        if os.path.exists(_path):
            # 读图片
            img = open(_path, 'rb')
            img_bytes = img.read()
            copy_img = open(copy_path, 'wb')
            self.status.meta[self.status.active_asset_text]["icon"] = img_bytes
            # 写图片
            # print(copy_path)

            copy_img.write(img_bytes)
            copy_img.close()
            img.close()
        self.Broadcast('/assloud/icon/update', None)

    def saveExport(self, _file):
        savepath = os.path.join(self.status.rootdir, self.status.active_bundle_text, self.status.active_asset_text,
                                "meta.json")
        try:
            f = open(savepath, 'w', encoding="utf-8")
            f.write(json.dumps(_file, indent=4, ensure_ascii=False))
            f.close()
            self.status.message = "保存成功"
            self.Broadcast('/assloud/message', None)
        except Exception as e:
            self.status.message = e
            self.Broadcast('/assloud/message', None)

    def openExcel(self, _file):
        if os.path.isfile(_file):
            self.status.exceldir = _file
            self.Broadcast('/assloud/file/open', None)

    # excel生成json文件
    def Generate(self, _flag):

        # TODO excel转json ——> 追加操作和更新操作

        excel_path = self.status.exceldir
        if _flag == "excel To json":
            self.status.meta = {}
            wbook = xlrd.open_workbook(excel_path)
            sheet_list = wbook.sheet_names()
            for sheet_name in sheet_list:
                sheet = wbook.sheet_by_name(sheet_name)
                nrow = sheet.nrows
                for i in range(1, nrow):
                    folder_id = sheet.cell_value(i, 1)

                    folder_name = folder_id + sheet.cell_value(i, 2)
                    # 如果excel格式不对
                    try:
                        # print(sheet.cell_value(i, 3), sheet.cell_type(i, 3))
                        self.status.meta["index"] = int(sheet.cell_value(i, 0))
                        self.status.meta["uri"] = sheet_name + '/' + sheet.cell_value(i, 2)
                        self.status.meta["alias"] = {"en_US": sheet.cell_value(i, 2)}
                        self.status.meta["title"] = {"en_US": sheet.cell_value(i, 2)}
                        self.status.meta["caption"] = {"en_US": str(sheet.cell_value(i, 3))}
                        self.status.meta["label"] = {"en_US": str(sheet.cell_value(i, 4))}
                        self.status.meta["topic"] = {"en_US": sheet.cell_value(i, 5)}
                        self.status.meta["description"] = {"en_US": sheet.cell_value(i, 6)}
                        self.status.meta["image2D"] = sheet.cell_value(i, 7)
                        self.status.meta["image3D"] = sheet.cell_value(i, 8)
                        self.status.meta["video2D"] = sheet.cell_value(i, 9)
                        self.status.meta["video3D"] = sheet.cell_value(i, 10)
                        self.status.meta["model"] = sheet.cell_value(i, 11)
                        self.status.meta["app"] = sheet.cell_value(i, 12)
                        self.status.meta["native"] = sheet.cell_value(i, 13)
                        self.status.meta["book"] = sheet.cell_value(i, 14)
                        self.status.meta["audio"] = sheet.cell_value(i, 15)
                        self.status.meta["qrCode"] = sheet.cell_value(i, 16)
                    except Exception as e:
                        self.status.message = "Excel文件格式有误"
                        self.Broadcast('/assloud/message', None)
                        return
                    # 创建以title命名的文件夹
                    save_path = os.path.join(os.path.expanduser('~'), "Desktop", 'Assloud/bundle', sheet_name,
                                             folder_name)
                    try:
                        os.makedirs(save_path)
                    except Exception as e:
                        pass
                        # print(e)
                    try:
                        f = open(os.path.join(save_path, "meta.json"), 'w', encoding="utf-8")
                        f.write(json.dumps(self.status.meta, indent=4, ensure_ascii=False))
                        f.close()
                        self.status.message = "生成成功"
                        self.Broadcast('/assloud/message', None)
                    except Exception as e:
                        self.status.message = f"未找到\"{sheet_name}\"目录"
                        self.Broadcast('/assloud/message', None)
                        return

        elif _flag == "json To excel":
            print("json To excel")
            # TODO json 转 excel

    def moveXma(self, _path):
        # exe_path = 'C:\\Users\\Tester\\Desktop'
        _path = os.path.abspath(os.path.join(_path, '..'))
        exe_path = os.path.join(_path, "source")
        if os.path.exists(exe_path):
            os.startfile(exe_path)
        else:
            os.mkdir(exe_path)
            os.startfile(exe_path)

    def addPic(self, _path):
        dir_name = self.status.active_asset.text()
        if re.search('_', dir_name):
            name = dir_name.split('_')[1]
        else:
            name = dir_name
        if len(name) > 5:
            dir_py = Pinyin().get_initials(name, splitter='').lower()
        else:
            dir_py = Pinyin().get_pinyin(name, splitter='')
        pic_path = os.path.join(_path, self.status.active_bundle_text, '_app', dir_py)
        if os.path.exists(pic_path):
            os.startfile(pic_path)
        else:
            return
