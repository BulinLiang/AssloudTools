import json
import PyMVCS
import PyArchive
from PyQt5.QtCore import QFileInfo
from model.util import Util


class RingPhotography360MakerStatus(PyMVCS.Status):
    def __init__(self):
        super(RingPhotography360MakerStatus, self).__init__()
        self.binary = {}
        self.description = ''
        self.title = ''
        self.active = ''
        self.preloads = [{'type': 'Sprite', 'name': 'img', 'count': 0, 'suffix': '.jpg'}]


class RingPhotography360MakerModel(PyMVCS.Model):
    NAME = 'RingPhotography360MakerModel'

    def _setup(self):
        self.logger.Trace('RingPhotography360MakerModel.setup')
        self.status = RingPhotography360MakerStatus()

    def _dismantle(self):
        self.logger.Trace('RingPhotography360MakerModel.dismantle')

    def clean(self):
        self.status.binary = {}
        self.active = ''
        # 发广播给视图层清空ui
        self.Broadcast('/maker/RingPhotography360/clean', None)

    def saveAddPhotos(self, _files):
        for file in _files:
            filename = QFileInfo(file).fileName()
            # 忽略已存在的
            if filename in self.status.binary:
                continue
            # 缓存二进制数据
            f = open(file, 'rb')
            self.status.binary[filename] = f.read()
            f.close()
        # 更新ui，更新图片列表
        self.Broadcast('/maker/RingPhotography360/update', None)

    def updateActivateFile(self, _file):
        self.logger.Trace(f'activate file: {_file}')
        self.status.active = _file
        self.Broadcast('/maker/RingPhotography360/file/activated', _file)

    def saveTitle(self, _value):
        self.title = _value

    def saveDescription(self, _value):
        self.description = _value

    def saveExport(self, _outFile):
        self.status.preloads[0]['count'] = len(self.status.binary)
        writer = PyArchive.FileWriter()
        writer.Open(_outFile, True)
        # 写入文件
        idx = 0
        for filename in self.status.binary.keys():
            idx += 1
            writer.Write('img#{0}.jpg'.format(idx), self.status.binary[filename])
        writer.Write("app.asset", Util.fileToBytes('./template/RingPhotography360/app.asset'))
        writer.Write("app.lua", Util.fileToBytes('./template/RingPhotography360/app.lua'))
        writer.Write("config.lua", self.renderConfig())
        writer.Write("preloads.json", Util.stringToBytes(json.dumps(self.status.preloads)))
        writer.Close()

    def saveImport(self, _inFile):
        self.clean()
        reader = PyArchive.FileReader()
        reader.Open(_inFile)
        for filename in reader.ListEntries():
            self.status.binary[filename] = reader.Read(filename)
        reader.Close()
        self.Broadcast('/maker/RingPhotography360/update', None)

    def renderConfig(self):
        lines = ''
        f = open('./template/RingPhotography360/config.lua', 'r')
        scripts = f.read()
        f.close()
        # 替换变量
        scripts = scripts.replace("{{__count__}}", "{0}".format(len(self.status.binary)))
        scripts = scripts.replace("{{__description__}}", self.description)
        scripts = scripts.replace("{{__title__}}", self.title)
        # 转换成python bytes
        return Util.stringToBytes(scripts)
