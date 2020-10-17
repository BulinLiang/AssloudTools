class Controller:

    def Setup(self, _framework):
        self.logger = _framework.logger
        self.config = _framework.config
        self.controllerCenter = _framework.controllerCenter
        self.modelCenter = _framework.modelCenter
        self.viewCenter = _framework.viewCenter
        self.serviceCenter = _framework.serviceCenter
        self._setup()

    def Dismantle(self):
        self._dismantle()

    def _setup(self):
        pass

    def _dismantle(self):
        pass
