import json
import PyMVCS
import PyArchive
from PyQt5.QtCore import QFileInfo
from model.util import Util


class RecitingMakerStatus(PyMVCS.Status):
    def __init__(self):
        super(RecitingMakerStatus, self).__init__()
        self.audio = bytes(0)
        self.content = ''
        self.title = ''
        self.author = ''
        self.reciter = ''
        self.preloads = [{'type': 'AudioClip', 'name': 'audio', 'count': 1, 'suffix': '.ogg'}]


class RecitingMakerModel(PyMVCS.Model):
    NAME = 'RecitingMakerModel'

    def _setup(self):
        self.logger.Trace('RecitingMakerModel.setup')
        self.status = RecitingMakerStatus()

    def _dismantle(self):
        self.logger.Trace('RecitingMakerModel.dismantle')

    def clean(self):
        self.audio = bytes(0)
        self.content = ''

    def saveAudio(self, _file):
        fileinfo = QFileInfo(_file)
        filename = fileinfo.fileName()
        # 缓存二进制数据
        f = open(_file, 'rb')
        self.status.audio = f.read()
        f.close()

    def saveTitle(self, _text):
        self.status.title = _text

    def saveAuthor(self, _text):
        self.status.author = _text

    def saveReciter(self, _text):
        self.status.reciter = _text

    def saveContent(self, _text):
        self.status.content = _text

    def saveExport(self, _outFile):
        writer = PyArchive.FileWriter()
        writer.Open(_outFile, True)

        # 判断是否有朗诵音频
        if 0 != len(self.status.audio):
            writer.Write("audio#1.ogg", self.status.audio)
            writer.Write("preloads.json", Util.stringToBytes(json.dumps(self.status.preloads)))
        else:
            writer.Write("preloads.json", Util.stringToBytes(json.dumps([])))

        # 写入所有文件
        writer.Write("app.asset", Util.fileToBytes('./template/Reciting/app.asset'))
        writer.Write("app.lua", Util.fileToBytes('./template/Reciting/app.lua'))
        writer.Write("config.lua", self.renderConfig())

        writer.Close()

    def saveImport(self, _inFile):
        self.clean()
        reader = PyArchive.FileReader()
        reader.Open(_inFile)
        # TODO 解析文件
        reader.Close()
        self.Broadcast('/maker/Reciting/update', None)

    def renderConfig(self):
        f = open('./template/Reciting/config.lua', 'r')
        scripts = f.read()
        f.close()
        # 替换变量
        scripts = scripts.replace("{{__title__}}", self.status.title)
        scripts = scripts.replace("{{__author__}}", self.status.author)
        scripts = scripts.replace("{{__reciter__}}", self.status.reciter)
        scripts = scripts.replace("{{__content__}}", self.status.content)
        # 转换成python bytes
        return Util.stringToBytes(scripts)
