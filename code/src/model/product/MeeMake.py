import PyMVCS
from PyQt5.QtCore import QFileInfo  # 获取文件信息，文件名，扩展名，路径等
from model.util import Util

class MeeMakeProductStatus(PyMVCS.Status):
    def __init__(self):
        super(MeeMakeProductStatus, self).__init__()
        # self.preloads = [{"type": "AudioClip", "name": "audio", "count": 2, "suffix": ".ogg"}]


class MeeMakeProductModel(PyMVCS.Model):
    NAME = "MeeMakeProductModel"

    def _setup(self):
        self.logger.Trace("MeeMakeProductModel.setup")
        self.status = MeeMakeProductStatus()

    def _dismantle(self):
        self.logger.Trace("MeeMakeProductModel.dismantle")
