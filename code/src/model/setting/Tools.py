import PyMVCS
import PyArchive  # 封装解封文件
import os
import re
import json
from PyQt5.QtCore import QFileInfo


class ToolsSettingStatus(PyMVCS.Status):
    def __init__(self):
        super(ToolsSettingStatus, self).__init__()
        self.pack_binary = {}
        self.unpack_binary = {}
        self.dynamic_binary = {}
        self.save_name = ''
        self.clean_sign = ''
        self.preloads = [{"type": "Package", "name": "file", "count": 0, "suffix": ""}]


class ToolsSettingModel(PyMVCS.Model):
    NAME = "ToolsSettingModel"

    def _setup(self):
        self.logger.Trace("ToolsSettingModel.setup")
        self.status = ToolsSettingStatus()

    def _dismantle(self):
        self.logger.Trace("ToolsSettingModel.dismantle")

    def clean(self):
        self.status.save_name = ''
        if self.status.clean_sign == 'pack':
            self.status.pack_binary = {}
        elif self.status.clean_sign == 'unpack':
            self.status.unpack_binary = {}
        elif self.status.clean_sign == 'dynamic':
            self.status.dynamic_binary = {}
        # 发广播给视图层清空ui
        self.Broadcast(f'/setting/tools/clean', None)

    def packAddFiles(self, _files):
        self.status.clean_sign = 'pack'
        self.clean()
        self.status.save_name = _files[0].split('/')[-2]
        for file_path in _files:
            file_name = QFileInfo(file_path).fileName()
            # 忽略已存在的
            if file_name in self.status.pack_binary.keys():
                continue
            # 缓存二进制数据
            with open(file_path, 'rb') as f:
                self.status.pack_binary[file_name] = f.read()
        self.Broadcast('/setting/tools/pack/update', None)

    def packExportFiles(self, _type):
        out_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'out_' + self.status.save_name + _type)
        writer = PyArchive.FileWriter()
        writer.Open(out_path, True)
        # 写入文件
        for file_name in self.status.pack_binary.keys():
            writer.Write(file_name, self.status.pack_binary[file_name])
        writer.Close()

    def unpackAddFiles(self, _inFile):
        self.status.clean_sign = 'unpack'
        self.clean()
        self.status.save_name = QFileInfo(_inFile).fileName().rsplit('.', 1)[0]
        reader = PyArchive.FileReader()
        reader.Open(_inFile)
        for filename in reader.ListEntries():
            self.status.unpack_binary[filename] = reader.Read(filename)
        reader.Close()
        self.Broadcast('/setting/tools/unpack/update', None)

    def unpackExportFiles(self):
        save_name = self.status.save_name  # 保存文件名
        unpack_binary = self.status.unpack_binary  # 数据字典
        # 解析文件，获取输出文件路径和文件二进制数据字典
        file_binary = self.analysisFiles(save_name, unpack_binary)
        for out_path, file_data in file_binary.items():
            with open(out_path, 'wb') as f:
                f.write(file_data)

    def dynamicAddFiles(self, _inFiles):
        self.status.clean_sign = 'dynamic'
        self.clean()
        # 添加文件，存入路径和对应数据
        for file_path in _inFiles:
            key_name = QFileInfo(file_path).fileName()
            # 读取该文件里面的文件数据
            reader = PyArchive.FileReader()
            reader.Open(file_path)
            self.status.dynamic_binary[key_name] = {}
            for filename in reader.ListEntries():
                # {根文件名 : {资源文件名 : 资源数据}}
                self.status.dynamic_binary[key_name][filename] = reader.Read(filename)
            reader.Close()
        self.Broadcast('/setting/tools/dynamic/update', None)

    def dynamicExportFiles(self, _files, _img):
        # 解析文件并输出（添加_dynamic.json）
        '''
            解析_manifest.json文件
        '''
        count = _files.count()
        file_list = [_files.item(i).text() for i in range(count)]
        # 动态加载的全景图名字列表{文件名:[图片名列表]}
        for root_name in file_list:
            manifest_data = self.status.dynamic_binary[root_name]["_manifest.json"]
            # 取出来为二进制数据，需进行转换，bytes --> str --> list
            manifest_data = json.loads(bytes.decode(manifest_data))
            img_list = []  # 图片名列表
            for manifest in manifest_data:
                img_name = manifest['theme']['skybox']
                extension = img_name.rsplit('.', 1)[1]  # 扩展名
                if extension in _img:
                    img_list.append(img_name)
                # 将_dynamic.json数据加入self.status.dynamic_binary[文件名]中
                self.status.dynamic_binary[root_name]['_dynamic.json'] = bytes(json.dumps(img_list), encoding='utf-8')
            # 读取文件名root_name重新打包文件
            out_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'dynamic_' + root_name)
            writer = PyArchive.FileWriter()
            writer.Open(out_path, True)
            # 取出root_name对应的数据写入文件
            for file_name in self.status.dynamic_binary[root_name].keys():
                writer.Write(file_name, self.status.dynamic_binary[root_name][file_name])
            writer.Close()

    def analysisFiles(self, _file, _binary):
        dir = os.path.join(os.path.expanduser('~'), 'Desktop', _file)
        if not os.path.exists(dir):
            os.makedirs(dir)
        # 解析文件
        out_binary = {}
        for file_name, file_data in _binary.items():
            if re.search('file://', file_name):
                file_name = re.sub('file://', '{{file}}', file_name)
                out_path = os.path.join(dir, file_name)
            else:
                out_path = os.path.join(dir, file_name)
            out_binary[out_path] = file_data
        return out_binary
