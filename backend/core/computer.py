from .cpu import CPU
from ..components.ram import RAM

class Computer:
    def __init__(self, ram_size=256):
        self.ram = RAM(ram_size)
        self.cpu = CPU(self.ram)

    def load_program(self, program_code, start_address=0):
        for i, byte in enumerate(program_code):
            self.ram.write(start_address + i, byte)
            
    def get_full_status(self):
        return f"CPU State:\n  Halted: {self.cpu.halted}\n  Registers: {self.cpu.rf.read_all()}\n" \
               f"RAM (first 16 bytes):\n  {[hex(self.ram.read(i)) for i in range(16)]}"

    def run_single_macro_step(self):
        """
        (保留) 为旧的命令行版本 main.py 执行一条完整的宏指令。
        这个方法不会产生微指令状态。
        """
        if self.cpu.halted:
            return
        
        # 这是一个简化的执行逻辑，仅用于兼容旧版
        # 实际的微指令执行在 run_micro_step_generator 中
        pc_val = self.cpu.rf.PC.read()
        instruction = self.ram.read(pc_val)
        self.cpu.rf.PC.write(pc_val + 1)
        opcode = self.cpu.control_unit.decode(instruction)
        self.cpu.control_unit.execute(opcode, self.cpu.rf, self.ram, self.cpu.alu, self.cpu)

    def get_micro_step_generator(self):
        """
        (新增) 这是给新版GUI的接口。
        它返回CPU核心的微指令步骤生成器。
        """
        return self.cpu.run_micro_step_generator()

    def reset(self):
        self.cpu.reset()
        self.ram.reset()