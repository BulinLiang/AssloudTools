import PyMVCS


class AuthStatus(PyMVCS.Status):
    def __init__(self):
        super(AuthStatus, self).__init__()
        self.code = 2
        self.token = ''
        self.message = ''


class AuthModel(PyMVCS.Model):
    NAME = 'AuthModel'

    def _setup(self):
        self.logger.Trace('AuthModel.setup')
        self.status = AuthStatus()

    def _dismantle(self):
        self.logger.Trace('AuthModel.dismantle')

    def UpdateToken(self, _status):
        self.status.code = _status.code
        self.status.token = _status.token
        self.status.message = _status.message
        self.Broadcast('/auth/token/update', None)

    def LoginError(self, _status):
        self.status.code = _status.code
        self.status.token = _status.token
        self.status.message = _status.message
        self.Broadcast('/auth/login/error', None)
