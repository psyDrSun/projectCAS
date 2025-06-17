from .register import Register

DEFAULT_HEX_ROM = {0x00: "03A001"}

class ControlUnit:
    """
    模拟微程序控制器。
    它根据当前指令和状态，决定下一个微操作。
    """
    def __init__(self):
        self.uPC = Register("uPC") # 微程序计数器

    def sequence(self, ir_val: int, cy_flag: int):
        """
        微程序定序逻辑。
        根据指令和标志位决定下一个微地址 (uPC)。
        """
        current_upc = self.uPC.read()
        
        # 定义所有微程序流的终点微地址
        terminal_addresses = {0x14, 0x16, 0x18, 0x1B, 0x1F, 0x20, 0x24}
        
        if current_upc in terminal_addresses:
            self.uPC.write(0)  # 返回取指周期
            return
        
        # 跳转逻辑
        next_upc = 0
        if current_upc == 1:  # 取指完成，进入指令译码
            op_code_group = (ir_val >> 6) & 0b11
            op_code_low = (ir_val >> 4) & 0b11
            if op_code_group == 0:
                next_upc = 0x02  # 所有访存指令进入公共取操作数序列
            elif op_code_group == 1: next_upc = 0x14 + op_code_low
            elif op_code_group == 2: next_upc = 0x18 + op_code_low
            else: next_upc = 0x1C + op_code_low
        elif current_upc == 0x05:  # 访存指令译码
            op_code_low = (ir_val >> 4) & 0b11
            if op_code_low == 0b11:  # BZC
                 next_upc = 0x23
            else:  # LDA/STA/JMP
                 next_upc = 0x20
        elif current_upc == 0x23:  # BZC 条件判断
            next_upc = 0x24 if cy_flag == 1 else 0
        else:  # 默认顺序执行
            next_upc = current_upc + 1

        self.uPC.write(next_upc)

    def reset(self):
        """重置控制单元状态。"""
        self.uPC.reset()