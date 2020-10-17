from service.meex import Request

class Service:

    def Setup(self, _framework):
        self.useMock = False
        self.mockProcessor = None
        self.logger = _framework.logger
        self.config = _framework.config
        self.modelCenter = _framework.modelCenter
        self.serviceCenter = _framework.serviceCenter
        self._setup()

    def Dismantle(self):
        self._dismantle()

    def _post(self, _url, _params, _onReply, _onError, _options):
        self.logger.Debug('post %s' % (_url))
        if self.useMock:
            if self.mockProcessor:
                res = Request(_url, _params)
                _options = res.post()
                self.mockProcessor(_url, 'POST', _params, _onReply, _onError, _options)
        else:
            pass

    def _get(self, _url, _params, _onReply, _onError, _options):
        self.logger.Debug('get %s', _url)
        if self.useMock:
            if self.mockProcessor:
                self.mockProcessor(_url, 'POST', _params, _onReply, _onError, _options)
        else:
            pass

    def _setup(self):
        pass

    def _dismantle(self):
        pass
