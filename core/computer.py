from .cpu import CPU
from components.ram import RAM

class Computer:
    """
    顶层计算机类。
    它封装了CPU和RAM，并提供了运行程序的接口。
    """
    def __init__(self):
        self.cpu = CPU()
        self.ram = RAM()

    def load_program(self, program: list, start_address: int = 0):
        """将程序（机器码列表）加载到内存中。"""
        for i, instruction in enumerate(program):
            self.ram.write(start_address + i, instruction)

    def run_single_macro_step(self):
        """
        完整地执行一条宏指令（由多条微指令构成）。
        """
        if self.cpu.halted or self.cpu.cu.uPC.read() != 0:
            return
        
        # 循环执行微指令，直到uPC返回0（表示一条宏指令执行完毕）
        while True:
            self.cpu.clock_tick(self.ram)
            if self.cpu.cu.uPC.read() == 0 or self.cpu.halted:
                break
    
    def reset(self):
        """重置整台计算机的状态。"""
        self.cpu.reset()
        self.ram.reset()

    def get_full_status(self) -> str:
        """获取并格式化计算机当前的所有状态，用于显示。"""
        rf = self.cpu.rf
        status = "================ STATUS ================\n"
        status += f"HALTED: {self.cpu.halted}\n"
        status += f"{rf.PC} {rf.IR}\n"
        status += f"{rf.AR}  {rf.FLAGS}\n"
        status += f"{rf.R0}   {rf.R1}   {rf.R2}\n"
        status += f"DR1: 0x{rf.DR1.read():02X}, DR2: 0x{rf.DR2.read():02X}, BUS: 0x{self.cpu.bus:02X}\n"
        status += f"uPC: 0x{self.cpu.cu.uPC.read():02X}\n"
        status += f"RAM[0x00-0x0F]: {' '.join([f'{val:02X}' for val in self.ram.memory[0:16]])}\n"
        status += "========================================"
        return status