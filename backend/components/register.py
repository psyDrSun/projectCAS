class Register:
    def __init__(self, name, size=8):
        self.name = name
        self.size = size
        self.value = 0

    def read(self):
        return self.value

    def write(self, value):
        mask = (1 << self.size) - 1
        self.value = value & mask

    def reset(self):
        self.value = 0

class RegisterFile:
    def __init__(self):
        self.PC = Register("PC")
        self.ACC = Register("ACC")
        self.IR = Register("IR")
        self.MAR = Register("MAR")
        self.MDR = Register("MDR")
        self.FLAG = Register("FLAG")
    
    def reset(self):
        for reg in self.__dict__.values():
            reg.reset()

    def read_all(self):
        """
        返回一个包含所有寄存器当前值的字典。
        这是前端渲染所需的核心数据之一。
        """
        return {name: reg.read() for name, reg in self.__dict__.items()}
