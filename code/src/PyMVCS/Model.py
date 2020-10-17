class Status:
    def __init__(self):
        self.code = 0
        self.message = ''

class Model:

    def Setup(self, _framework):
        self.logger = _framework.logger
        self.config = _framework.config
        self.modelCenter = _framework.modelCenter
        self.controllerCenter = _framework.controllerCenter
        self.status = None
        self._setup()

    def Dismantle(self):
        self._dismantle()

    def Broadcast(self, _action, _data):
        self.modelCenter.broadcast(_action, self.status, _data)


    def _setup(self):
        pass

    def _dismantle(self):
        pass
