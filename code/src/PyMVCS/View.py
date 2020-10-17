class View:
    def Setup(self, _framework):
        self.handlers = {}
        self.logger = _framework.logger
        self.config = _framework.config
        self.viewCenter = _framework.viewCenter
        self.modelCenter = _framework.modelCenter
        self.serviceCenter = _framework.serviceCenter
        self._setup()

    def Dismantle(self):
        self._dismantle()

    def Route(self, _action, _handler):
        self.handlers[_action] = _handler

    def handle(self, _action, _status, _data):
        if _action in self.handlers:
            self.handlers[_action](_status, _data)

    def _setup(self):
        pass

    def _dismantle(self):
        pass
