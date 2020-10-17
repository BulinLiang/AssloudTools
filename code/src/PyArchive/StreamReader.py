from .Entry import Entry
from .Reader import Reader

class StreamReader(Reader):
    """
    """

    def __init__(self):
        self._entryMap = {}
        self._stream = None
        self._offset = 0
        self._size = 0

    def ListEntries(self):
        return self._entryMap.keys()

    def Read(self, _path):
        """ 读取项目
        Agrs:
            _path: 路径
        Returns:
            byte[]: 文件数据
        """

        if None == self._stream:
            return None
        if not _path in self._entryMap:
            return None
        entry = self._entryMap[_path]
        self._stream.seek(self._entryMap[_path].offset)
        return self.readBytes(self._entryMap[_path].size)

    def Close(self):
        self._stream.close()

    def parseHeader(self):
        totalSize = self.readInt64()
        flag = self.readInt64()
        vTableOffset = self.readInt64()
        vTableSize = self.readInt64()

        if not self._size == totalSize:
            raise ("archive want %d bytes, but only has %d bytes", totalSize, self._size)

        self._stream.seek(vTableOffset)
        count = self.readInt32()
        for i in range(0, count):
            entry = Entry()
            length = self.readInt32()
            entryPath = self.readString(length)
            entry.offset = self.readInt64()
            entry.size = self.readInt64()
            self._entryMap[entryPath] = entry

    def readInt32(self):
        buffer = self._stream.read(4)
        return self.bytesToInt32(buffer)

    def readInt64(self):
        buffer = self._stream.read(8)
        return self.bytesToInt64(buffer)

    def readString(self, _size):
        buffer = self._stream.read(_size)
        return self.bytesToString(buffer)

    def readBytes(self, _size):
        return self._stream.read(_size)

