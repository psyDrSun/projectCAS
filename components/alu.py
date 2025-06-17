class ALU:
    """
    模拟算术逻辑单元 (Arithmetic Logic Unit)。
    它不存储任何状态，仅根据输入和控制信号执行计算。
    """
    def __init__(self):
        self.carry_out = 0

    def execute(self, s_val: int, m_val: int, cn_val: int, in1: int, in2: int) -> int:
        """
        执行一次ALU操作。
        :param s_val: 操作选择码 (S0-S3)
        :param m_val: 模式选择 (1=算术, 0=逻辑)
        :param cn_val: 输入进位
        :param in1: 第一个操作数
        :param in2: 第二个操作数
        :return: 8位计算结果
        """
        self.carry_out = 0
        raw_result = 0
        
        in1 &= 0xFF
        in2 &= 0xFF
        cn_val &= 0x01

        if m_val == 1:  # 算术运算
            if s_val == 0b1001:  # ADC
                raw_result = in1 + in2 + cn_val
        else:  # 逻辑运算
            if s_val == 0b0110:  # COM (NOT)
                raw_result = ~in1
            elif s_val == 0b1011:  # AND
                raw_result = in1 & in2
        
        if raw_result > 0xFF:
            self.carry_out = 1
            
        return raw_result & 0xFF