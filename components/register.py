class Register:
    """
    模拟一个8位寄存器。
    这是计算机中最基本的存储单元。
    """
    def __init__(self, name="REG"):
        self.name = name
        self.value = 0

    def write(self, new_value: int):
        """向寄存器写入一个值 (自动处理8位截断)。"""
        self.value = int(new_value) & 0xFF

    def read(self) -> int:
        """从寄存器读取当前值。"""
        return self.value
    
    def increment(self):
        """将寄存器的值加一。"""
        self.value = (self.value + 1) & 0xFF

    def reset(self):
        """将寄存器的值清零。"""
        self.value = 0

    def __repr__(self) -> str:
        """提供一个便于调试的字符串表示形式。"""
        return f"{self.name}: 0x{self.value:02X} (0b{self.value:08b})"