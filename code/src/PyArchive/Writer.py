class Writer:

    def int32ToBytes(self, _value):
        buffer = bytearray(4)
        buffer[0] = (_value & 0xff)
        buffer[1] = (_value & 0xff00) >> 8
        buffer[2] = (_value & 0xff0000) >> 16
        buffer[3] = (_value & 0xff000000) >> 24
        return buffer

    def int64ToBytes(self, _value):
        buffer = bytearray(8)
        buffer[0] = (_value & 0xff)
        buffer[1] = (_value & 0xff00) >> 8
        buffer[2] = (_value & 0xff0000) >> 16
        buffer[3] = (_value & 0xff000000) >> 24
        buffer[4] = (_value & 0xff00000000 )>> 32
        buffer[5] = (_value & 0xff0000000000) >> 40
        buffer[6] = (_value & 0xff000000000000) >> 48
        buffer[7] = (_value & 0xff00000000000000) >> 56
        return buffer

    def stringToBytes(self, _value):
        return _value.encode("utf-8")
