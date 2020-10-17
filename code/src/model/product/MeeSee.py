import PyMVCS
from PyQt5.QtCore import QFileInfo  # 获取文件信息，文件名，扩展名，路径等
from model.util import Util

class MeeSeeProductStatus(PyMVCS.Status):
    def __init__(self):
        super(MeeSeeProductStatus, self).__init__()
        # self.preloads = [{"type": "AudioClip", "name": "audio", "count": 2, "suffix": ".ogg"}]


class MeeSeeProductModel(PyMVCS.Model):
    NAME = "MeeSeeProductModel"

    def _setup(self):
        self.logger.Trace("MeeSeeProductModel.setup")
        self.status = MeeSeeProductStatus()

    def _dismantle(self):
        self.logger.Trace("MeeSeeProductModel.dismantle")
