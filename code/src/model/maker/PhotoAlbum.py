import json
import PyMVCS
import PyArchive
from PyQt5.QtCore import QFileInfo
from model.util import Util


class PhotoAlbumMakerStatus(PyMVCS.Status):
    def __init__(self):
        super(PhotoAlbumMakerStatus, self).__init__()
        self.token = ''
        # 相册： key 文件名， value 照片描述
        self.photos = {}
        # key 文件名， value 图片二进制数据
        self.binary = {}
        self.active = ''
        self.preloads = [{'type': 'Sprite', 'name': 'img', 'count': 0, 'suffix': '.jpg'}]


class PhotoAlbumMakerModel(PyMVCS.Model):
    NAME = 'PhotoAlbumMakerModel'

    def _setup(self):
        self.logger.Trace('PhotoAlbumMakerModel.setup')
        self.status = PhotoAlbumMakerStatus()

    def _dismantle(self):
        self.logger.Trace('PhotoAlbumMakerModel.dismantle')

    def clean(self):
        self.status.photos = {}
        self.status.binary = {}
        self.status.active = ''
        # 发广播给视图层清空ui
        self.Broadcast('/maker/photoalbum/clean', None)

    def saveAddPhotos(self, _files):
        for file in _files:
            filename = QFileInfo(file).fileName()
            # 忽略已存在的
            if filename in self.status.photos:
                continue
            # 加入字典，描述默认为空
            self.status.photos[filename] = ""
            # 缓存二进制数据
            f = open(file, 'rb')
            self.status.binary[filename] = f.read()
            f.close()

        # print(self.status.photos.keys())
        self.Broadcast('/maker/photoalbum/update', None)

    def updateActivateFile(self, _file):
        self.logger.Trace(f'activate file: {_file}')
        self.status.active = _file
        self.Broadcast('/maker/photoalbum/file/activated', None)

    # 当照片描述ui发生更改时将会触发此函数，如添加文字，清空
    def saveText(self, _text):
        # 判断是否选中照片
        if self.status.active == '':
            return

        self.status.photos[self.status.active] = _text
        # print(self.status.photos[self.status.active])
    def saveExport(self, _outFile):
        self.status.preloads[0]['count'] = len(self.status.photos)
        writer = PyArchive.FileWriter()
        writer.Open(_outFile, True)
        # 写入文件
        idx = 0
        for filename in self.status.binary.keys():
            idx += 1
            writer.Write('img#{0}.jpg'.format(idx), self.status.binary[filename])
        writer.Write("app.asset", Util.fileToBytes('./template/PhotoAlbum/app.asset'))
        writer.Write("app.lua", Util.fileToBytes('./template/PhotoAlbum/app.lua'))
        writer.Write("config.lua", self.renderConfig())
        writer.Write("preloads.json", Util.stringToBytes(json.dumps(self.status.preloads)))
        writer.Close()

    def saveImport(self, _inFile):
        self.clean()
        reader = PyArchive.FileReader()
        reader.Open(_inFile)
        for filename in reader.ListEntries():
            self.status.photos[filename] = ""
            self.status.binary[filename] = reader.Read(filename)
        reader.Close()
        self.Broadcast('/maker/photoalbum/update', None)

    def renderConfig(self):
        lines = ''
        idx = 0
        for desc in self.status.photos.values():
            idx += 1
            line = 'description["img#{0}.jpg"]["en_US"] = "{1}"\n'.format(idx, desc)
            lines += line
        f = open('./template/PhotoAlbum/config.lua', 'r')
        scripts = f.read()
        f.close()
        # 替换变量
        scripts = scripts.replace("{{__count__}}", "{0}".format(len(self.status.photos)))
        scripts = scripts.replace("{{__description__}}", lines)
        # 转换成python bytes
        return Util.stringToBytes(scripts)
