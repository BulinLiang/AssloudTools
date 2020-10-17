class Reader:
    """
    """

    def bytesToInt32(self, _value):
        """
        Args:
            _value: 字节数组
        Returns:
            int32: 32位整型值

        """
        value = 0 
        value |= _value[0] & 0xff
        value |= ((_value[1]) << 8 ) & 0xff00
        value |= ((_value[2]) << 16 ) & 0xff0000
        value |= ((_value[3]) << 24 ) & 0xff000000
        return value

    def bytesToInt64(self, _value):
        """
        Args:
            _value: 字节数组
        Returns:
            int63: 64位整型值

        """
        value = 0
        value |= _value[0] & 0xff
        value |= ((_value[1]) << 8 ) & 0xff00
        value |= ((_value[2]) << 16 ) & 0xff0000
        value |= ((_value[3]) << 24 ) & 0xff000000
        value |= ((_value[4]) << 32 ) & 0xff00000000
        value |= ((_value[5]) << 40 ) & 0xff0000000000
        value |= ((_value[6]) << 48 ) & 0xff000000000000
        value |= ((_value[7]) << 56 ) & 0xff00000000000000
        return value

    def bytesToString(self, _value):
        return _value.decode("utf-8")
