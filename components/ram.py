class RAM:
    """
    模拟随机存取存储器 (Random Access Memory)。
    """
    def __init__(self, size=256):
        self.size = size
        self.memory = [0] * size

    def write(self, address: int, value: int):
        """向指定内存地址写入一个字节。"""
        if 0 <= address < self.size:
            self.memory[address] = int(value) & 0xFF

    def read(self, address: int) -> int:
        """从指定内存地址读取一个字节。"""
        if 0 <= address < self.size:
            return self.memory[address]
        return 0
    
    def reset(self):
        """将所有内存单元清零。"""
        self.memory = [0] * self.size