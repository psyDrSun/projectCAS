class ControlUnit:
    """
    The Control Unit (CU) is responsible for decoding instructions
    and orchestrating the CPU's components to execute them.
    """
    def __init__(self):
        # Defines the instruction set architecture (ISA)
        # Key is the 4-bit opcode.
        self.OPCODES = {
            0x0: {'name': 'NOP', 'args': 0},
            0x1: {'name': 'LDA', 'args': 1}, # Load Accumulator from memory
            0x2: {'name': 'STA', 'args': 1}, # Store Accumulator to memory
            0x3: {'name': 'ADD', 'args': 1}, # Add memory to Accumulator
            0x4: {'name': 'IN', 'args': 0},  # Input to Accumulator
            0x5: {'name': 'OUT', 'args': 0}, # Output from Accumulator
            0x6: {'name': 'JMP', 'args': 1}, # Unconditional Jump
            0x7: {'name': 'JZ', 'args': 1},  # Jump if Zero flag is set
            0x8: {'name': 'JC', 'args': 1},  # Jump if Carry flag is set
            0xF: {'name': 'HALT', 'args': 0},# Halt the CPU
        }

    def decode(self, instruction_code: int) -> dict:
        """
        Decodes a raw instruction byte into a dictionary.
        This is the missing method that caused the crash.
        """
        if not isinstance(instruction_code, int):
            return self.OPCODES[0x0] # Return NOP for invalid input

        opcode_val = (instruction_code & 0xF0) >> 4
        operand = instruction_code & 0x0F

        # Find the instruction details from the ISA definition
        instruction_details = self.OPCODES.get(opcode_val, self.OPCODES[0x0]) # Default to NOP
        instruction_details['operand'] = operand
        return instruction_details

    def execute(self, opcode: dict, rf, ram, alu, cpu_instance):
        """
        Executes the logic for a decoded instruction.
        This method's logic should be filled out to handle each instruction.
        """
        op_name = opcode.get('name')
        operand = opcode.get('operand')

        # This is where the detailed logic for each instruction would go.
        # For our current visualization, the core logic is handled by the
        # micro-step generator in cpu.py. This method can be expanded later.
        if op_name == 'HALT':
            cpu_instance.halted = True
        
        # Example of how other instructions would be handled here in a non-visual run.
        # elif op_name == 'LDA':
        #     rf.ACC.write(ram.read(operand))
        # elif op_name == 'ADD':
        #     val = ram.read(operand)
        #     alu.add(val)
        
        pass