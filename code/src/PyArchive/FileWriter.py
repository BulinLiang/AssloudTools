import os
from .Entry import Entry
from .StreamWriter import StreamWriter

class FileWriter(StreamWriter):
    """
    Attributes:
        
    """
    def Open(self, _filepath, _overwrite):
        if os.path.isfile(_filepath):
            if _overwrite:
                os.remove(_filepath)
            else:
                return

        self._entryMap.clear()
        # 以二进制写入模式打开文件，并保存句柄
        self._stream = open(_filepath, 'wb')
        # 写入数据头
        # 依次为 整个文件尺寸、标识、映射表偏移、映射表尺寸
        # | total size | flag  | vtable offset | vtable size |
        # | int64      | int64 | int64         | int64       |
        self.writeInt64(0)
        self.writeInt64(0)
        self.writeInt64(0)
        self.writeInt64(0)
