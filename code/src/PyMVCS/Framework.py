# -*- coding: utf-8 -*-

from .ModelCenter import ModelCenter
from .ViewCenter import ViewCenter
from .ControllerCenter import ControllerCenter
from .ServiceCenter import ServiceCenter

class Framework:

    def __init__(self, _config, _logger):
        self.config = _config
        self.logger = _logger

    # 实例化各层中心
    def Initialize(self):
        self.logger.Info('Initialize PyMVCS')
        self.viewCenter = ViewCenter(self)
        self.controllerCenter = ControllerCenter(self)
        self.modelCenter = ModelCenter(self)
        self.serviceCenter = ServiceCenter(self)

    # 装载部件
    # 调用所有部件的setup方法
    def Setup(self):
        self.logger.Info('Setup PyMVCS')
        self.viewCenter.Setup()
        self.controllerCenter.Setup()
        self.modelCenter.Setup()
        self.serviceCenter.Setup()

    # 拆卸部件
    # 调用所有部件的dismantle方法
    def Dismantle(self):
        self.logger.Info('Dismantle PyMVCS')
        self.serviceCenter.Dismantle()
        self.modelCenter.Dismantle()
        self.controllerCenter.Dismantle()
        self.viewCenter.Dismantle()

    # 销毁各层中心
    def Release(self):
        self.logger.Info('Release PyMVCS')
        self.serviceCenter = None
        self.modelCenter = None
        self.controllerCenter = None
        self.viewCenter = None


