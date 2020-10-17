class Util:

    def stringToBytes(_value):
        return _value.encode("utf-8")

    def bytesToString(_value):
        return _value.decode("utf-8")

    def fileToBytes(_file):
        f = open(_file, 'rb')
        data = f.read()
        f.close()
        return data
