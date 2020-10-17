# -*- coding: utf-8 -*-

class ServiceCenter:

    def __init__(self, _framework):
         self.__framework = _framework
         self.services= {}

    def Register(self, _uuid, _service):
        self.__framework.logger.Info('register service %s'%(_uuid))
        if _uuid in self.services:
            raise KeyError('service is exists')
        self.services[_uuid] = _service

    def Cancel(self, _uuid):
        self.__framework.logger.Info('cancel service %s'%(_uuid))
        if not _uuid in self.services:
            raise KeyError('service not found')
        del self.services[_uuid] 

    def Find(self, _uuid):
        return self.services[_uuid]

    def Setup(self):
        for v in self.services.values():
            v.Setup(self.__framework)

    def Dismantle(self):
        for v in self.services.values():
            v.Dismantle()

