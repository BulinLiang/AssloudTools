# -*- coding: utf-8 -*-

class ViewCenter:

    def __init__(self, _framework):
         self.__framework = _framework
         self.views = {}

    def Register(self, _uuid, _view):
        self.__framework.logger.Info('register view %s'%(_uuid))
        if _uuid in self.views:
            raise KeyError('view is exists')
        self.views[_uuid] = _view

    def Cancel(self, _uuid):
        self.__framework.logger.Info('cancel view %s'%(_uuid))
        if not _uuid in self.views:
            raise KeyError('view not found')
        del self.views[_uuid] 

    def Find(self, _uuid):
        return self.views[_uuid]

    def Setup(self):
        for v in self.views.values():
            v.Setup(self.__framework)

    def Dismantle(self):
        for v in self.views.values():
            v.Dismantle()

    def handleAction(self, _action, _status, _data):
        for v in self.views.values():
            v.handle(_action, _status, _data)


