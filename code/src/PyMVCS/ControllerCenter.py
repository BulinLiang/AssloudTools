# -*- coding: utf-8 -*-

class ControllerCenter:

    def __init__(self, _framework):
         self.__framework = _framework
         self.controllers = {}

    def Register(self, _uuid, _controller):
        self.__framework.logger.Info('register controller %s'%(_uuid))
        if _uuid in self.controllers:
            raise KeyError('controller is exists')
        self.controllers[_uuid] = _controller

    def Cancel(self, _uuid):
        self.__framework.logger.Info('cancel controller %s'%(_uuid))
        if not _uuid in self.controllers:
            raise KeyError('controller not found')
        del self.controllers[_uuid] 

    def Find(self, _uuid):
        return self.controllers[_uuid]

    def Setup(self):
        for v in self.controllers.values():
            v.Setup(self.__framework)

    def Dismantle(self):
        for v in self.controllers.values():
            v.Dismantle()

