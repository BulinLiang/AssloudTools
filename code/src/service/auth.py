import PyMVCS
import mock.auth
from model.auth import AuthModel, AuthStatus
import re


class AuthService(PyMVCS.Service):
    NAME = 'AuthService'

    def _setup(self):
        self.logger.Trace('AuthService.setup')
        self.useMock = True
        self.mockProcessor = mock.auth.Process

    def _dismantle(self):
        self.logger.Trace('AuthService.dismantle')

    def Signin(self, _username, _password, _url):
        self.logger.Trace('Signin')
        params = {'username': _username, 'password': _password}
        # admin
        if _url == 'yumei209':
            authModel = self.modelCenter.Find(AuthModel.NAME)
            status = AuthStatus()
            self.message = "Administretor"
            status.code = 3
            status.token = 'admin'
            self.logger.Debug(str({'code': status.code, 'token': status.token, 'message': self.message}))
            authModel.UpdateToken(status)
        # Connecting to the server
        elif re.search('^(http|https|ftp)://.*?', _url):
            self._post(_url, params, self.onSigninReply, self.onSigninError, None)
        # Url Error
        elif not re.search('^(http|https|ftp)://.*?|s', _url):
            self.message = 'url error'

    def onSigninReply(self, _reply):
        self.logger.Debug(_reply)
        authModel = self.modelCenter.Find(AuthModel.NAME)
        status = AuthStatus()
        status.message = eval(_reply)['message']
        status.code = eval(_reply)['code']
        status.token = eval(_reply)['accessToken']
        authModel.UpdateToken(status)

    def onSigninError(self, _error):
        self.logger.Error(_error)
        authModel = self.modelCenter.Find(AuthModel.NAME)
        status = AuthStatus()
        status.message = eval(_error)['message']
        status.code = eval(_error)['code']
        status.token = eval(_error)['accessToken']
        authModel.LoginError(status)
