import PyMVCS
import PyArchive
from PyQt5.QtCore import QFileInfo
from model.util import Util
import json

class KaraokeMakerStatus(PyMVCS.Status):
    def __init__(self):
        super(KaraokeMakerStatus, self).__init__()
        self.music = bytes(0)
        self.accompaniment = bytes(0)
        self.lyrics = ''
        self.preloads = [{'type': 'AudioClip', 'name': 'audio', 'count': 2, 'suffix': '.ogg'}]


class KaraokeMakerModel(PyMVCS.Model):
    NAME = 'KaraokeMakerModel'

    def _setup(self):
        self.logger.Trace('KaraokeMakerModel.setup')
        self.status = KaraokeMakerStatus()

    def _dismantle(self):
        self.logger.Trace('KaraokeMakerModel.dismantle')

    def clean(self):
        self.music = bytes(0)
        self.accompaniment = bytes(0)
        self.lyrics = ''

    def saveMusic(self, _file):
        fileinfo = QFileInfo(_file)
        filename = fileinfo.fileName()
        # 缓存二进制数据
        f = open(_file, 'rb')
        self.status.music = f.read()
        f.close()

    def saveAccompaniment(self, _file):
        fileinfo = QFileInfo(_file)
        filename = fileinfo.fileName()
        # 缓存二进制数据
        f = open(_file, 'rb')
        self.status.accompaniment = f.read()
        f.close()

    def saveLyrics(self, _text):
        self.status.lyrics = _text

    def saveExport(self, _outFile):
        writer = PyArchive.FileWriter()
        writer.Open(_outFile, True)

        # 写入所有文件
        writer.Write("audio#1.ogg", self.status.music)
        writer.Write("audio#2.ogg", self.status.accompaniment)
        writer.Write("app.asset", Util.fileToBytes('./template/Karaoke/app.asset'))
        writer.Write("app.lua", Util.fileToBytes('./template/Karaoke/app.lua'))
        writer.Write("config.lua", self.renderConfig())
        writer.Write("preloads.json", Util.stringToBytes(json.dumps(self.status.preloads)))
        writer.Close()

    def saveImport(self, _inFile):
        self.clean()
        reader = PyArchive.FileReader()
        reader.Open(_inFile)
        # TODO 解析文件
        reader.Close()
        self.Broadcast('/maker/Karaoke/update', None)

    def renderConfig(self):
        f = open('./template/Karaoke/config.lua', 'r')
        scripts = f.read()
        f.close()
        # 替换变量
        scripts = scripts.replace("{{__lrc__}}", self.status.lyrics)
        # 转换成python bytes
        return Util.stringToBytes(scripts)
