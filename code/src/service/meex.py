from urllib import request
import json


class Request:
    def __init__(self, _url, _params):
        self.url = _url
        self.params = _params

    def post(self):
        # post传入数据需要二进制，所以要将用户名密码的字典转换成字符再转成bytes
        try:
            res = request.urlopen(url=self.url, data=json.dumps(self.params).encode())
            data = json.loads(res.read().decode())
            # 登陆成功
            if data['status'] == {}:
                uuid = data['uuid']
                accessToken = data['accessToken']
                _options = {'code': 0, 'uuid': uuid, 'accessToken': accessToken, 'message': 'SigninSuccess'}
                return _options
            # 登录失败
            elif data['status'] != {}:
                message = data['status']['message']
                _options = {'code': 1, 'uuid': '', 'accessToken': '', 'message': message}
                return _options
        # 服务器错误
        except Exception as e:
            _options = {'code': 1, 'uuid': '', 'accessToken': '', 'message': str(e)}
            return _options

    def get(self):
        pass
