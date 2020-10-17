import PyMVCS

class AuthController(PyMVCS.Controller):
    NAME = 'AuthController'

    def setup(self):
        self.logger.Trace('AuthController.setup')

    def dismantle(self):
        self.logger.Trace('AuthController.dismantle')

