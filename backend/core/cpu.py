from ..components.register import Register
from ..components.alu import ALU
from ..components.control_unit import ControlUnit
from ..components.ram import RAM

class RegisterFile:
    """一个专门用于管理CPU内部所有寄存器的容器类。"""
    def __init__(self):
        self.R0 = Register("R0")
        self.R1 = Register("R1")
        self.R2 = Register("R2/RI")
        self.PC = Register("PC")
        self.IR = Register("IR")
        self.AR = Register("AR")
        self.DR1 = Register("DR1")
        self.DR2 = Register("DR2")
        self.FLAGS = Register("FLAGS")
        self.registers = [self.R0, self.R1, self.R2, self.R1]

    def get_reg_by_addr(self, addr: int) -> Register:
        return self.registers[addr & 0b11]

    def reset(self):
        for reg_name in self.__dict__:
            if isinstance(getattr(self, reg_name), Register):
                getattr(self, reg_name).reset()


class CPU:
    """
    模拟中央处理器 (Central Processing Unit)。
    它集成了寄存器文件、ALU和控制单元，并执行指令周期。
    """
    def __init__(self):
        self.rf = RegisterFile()
        self.alu = ALU()
        self.cu = ControlUnit()
        self.bus = 0
        self.input_device_val = 0
        self.output_device_val = 0
        self.halted = False

    def reset(self):
        self.rf.reset()
        self.cu.reset()
        self.bus = 0
        self.halted = False

    def execute(self, ram: RAM):
        """持续执行指令，直到CPU停止。"""
        while not self.halted:
            self.clock_tick(ram)

    def clock_tick(self, ram: RAM):
        """执行一个时钟周期（一个微指令）。"""
        if self.halted: return

        current_upc = self.cu.uPC.read()
        ir = self.rf.IR.read()
        rs_addr = (ir >> 2) & 0b11
        rd_addr = ir & 0b11

        # 根据微程序计数器 (uPC) 执行相应的微操作
        if current_upc == 0:  # 取指1: PC -> AR, PC+1
            self.rf.AR.write(self.rf.PC.read())
            self.rf.PC.increment()
        elif current_upc == 1:  # 取指2: RAM -> IR
            self.bus = ram.read(self.rf.AR.read())
            self.rf.IR.write(self.bus)
        
        # 访存指令公共序列
        elif current_upc == 2:  # 取偏移量D: PC -> AR, PC+1
            self.rf.AR.write(self.rf.PC.read())
            self.rf.PC.increment()
        elif current_upc == 3:  # D -> DR2
            self.bus = ram.read(self.rf.AR.read())
            self.rf.DR2.write(self.bus)
        elif current_upc == 4:  # 计算有效地址E
            addr_mode = (ir >> 2) & 0b11
            e = 0
            # 根据寻址模式计算有效地址
            if addr_mode == 0: e = self.rf.DR2.read()  # 直接
            elif addr_mode == 1: e = ram.read(self.rf.DR2.read())  # 间接
            elif addr_mode == 2: e = self.rf.R2.read() + self.rf.DR2.read()  # 变址
            elif addr_mode == 3: e = self.rf.PC.read() + self.rf.DR2.read()  # 相对
            self.rf.DR1.write(e & 0xFF)  # 暂存E
        elif current_upc == 5:  # E -> AR
            self.rf.AR.write(self.rf.DR1.read())

        # 具体指令执行
        elif current_upc == 0x20:  # LDA: RAM[E] -> RD
            self.bus = ram.read(self.rf.AR.read())
            self.rf.get_reg_by_addr(rd_addr).write(self.bus)
        elif current_upc == 0x14:  # IN: SW -> RD
            self.bus = self.input_device_val
            self.rf.get_reg_by_addr(rd_addr).write(self.bus)
        elif current_upc == 0x18:  # MOV: RS -> RD
            self.bus = self.rf.get_reg_by_addr(rs_addr).read()
            self.rf.get_reg_by_addr(rd_addr).write(self.bus)
        elif current_upc == 0x19:  # ADC Step 1
            self.bus = self.rf.get_reg_by_addr(rs_addr).read()
            self.rf.DR1.write(self.bus)
        elif current_upc == 0x1A:  # ADC Step 2
            self.bus = self.rf.get_reg_by_addr(rd_addr).read()
            self.rf.DR2.write(self.bus)
        elif current_upc == 0x1B:  # ADC Step 3
            cy_in = self.rf.FLAGS.read() & 1
            self.bus = self.alu.execute(0b1001, 1, cy_in, self.rf.DR1.read(), self.rf.DR2.read())
            if self.alu.carry_out: self.rf.FLAGS.write(self.rf.FLAGS.read() | 1)
            else: self.rf.FLAGS.write(self.rf.FLAGS.read() & ~1)
            self.rf.get_reg_by_addr(rd_addr).write(self.bus)
        elif current_upc == 0x1F:  # RLC
            reg = self.rf.get_reg_by_addr(rd_addr)
            val = reg.read()
            cy_in = self.rf.FLAGS.read() & 1
            new_cy = (val >> 7) & 1
            val = ((val << 1) | cy_in) & 0xFF
            reg.write(val)
            if new_cy: self.rf.FLAGS.write(1)
            else: self.rf.FLAGS.write(0)
        elif current_upc == 0x16:  # HALT
            self.halted = True
        elif current_upc == 0x24:  # JMP/BZC
            self.rf.PC.write(self.rf.AR.read())

        # 决定下一个微指令地址
        self.cu.sequence(self.rf.IR.read(), self.rf.FLAGS.read() & 1)
        
        def reset(self):
            """Resets all registers and the halted flag."""
            self.rf.PC.reset()
            self.rf.ACC.reset()
            self.rf.IR.reset()
            self.rf.MAR.reset()
            self.rf.MDR.reset()
            self.rf.FLAG.reset()
            self.halted = False
            self.input_device_val = 0