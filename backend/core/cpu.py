from ..components.alu import ALU
from ..components.control_unit import ControlUnit
from ..components.register import RegisterFile

class CPU:
    def __init__(self, ram):
        self.ram = ram
        self.rf = RegisterFile()
        # --- FIX ---
        # The ALU constructor does not take any arguments.
        # It operates on data passed to its 'execute' method.
        self.alu = ALU() 
        # -----------
        self.control_unit = ControlUnit()
        self.halted = False
        self.input_device_val = 0

    def reset(self):
        self.rf.reset()
        self.halted = False
        self.input_device_val = 0

    def _get_current_state(self, active_components=None, active_buses=None):
        """
        An internal helper function to package the current complete state.
        This is the single data structure that will be yielded to the frontend.
        """
        return {
            "registers": self.rf.read_all(),
            "halted": self.halted,
            "active_components": active_components or set(),
            "active_buses": active_buses or set(),
        }

    def run_micro_step_generator(self):
        """
        This is a generator that executes each micro-operation of a single macro-instruction step-by-step.
        After each micro-op, it yields the current state of the computer.
        """
        if self.halted:
            yield self._get_current_state(active_components={'CPU_HALTED'})
            return

        # --- 1. Fetch Cycle ---
        # T0: PC -> MAR
        pc_val = self.rf.PC.read()
        self.rf.MAR.write(pc_val)
        yield self._get_current_state(
            active_components={'PC', 'MAR'},
            active_buses={'PC_MAR_BUS', 'ADDR_BUS'}
        )

        # T1: M(MAR) -> MDR
        instruction_code = self.ram.read(self.rf.MAR.read())
        self.rf.MDR.write(instruction_code)
        yield self._get_current_state(
            active_components={'RAM', 'MDR'},
            active_buses={'DATA_BUS'}
        )

        # T2: MDR -> IR
        self.rf.IR.write(self.rf.MDR.read())
        yield self._get_current_state(
            active_components={'MDR', 'IR'},
            active_buses={'MDR_IR_BUS'}
        )

        # T3: PC++
        self.rf.PC.write(pc_val + 1)
        yield self._get_current_state(
            active_components={'PC', 'ALU'},
            active_buses={'PC_ALU_BUS'}
        )

        # --- 2. Decode & Execute Cycle ---
        opcode = self.control_unit.decode(self.rf.IR.read())
        
        yield self._get_current_state(active_components={'CU', 'IR'})

        # --- Execute micro-code for different instructions ---
        if opcode['name'] == 'LDA':
            # Simplified micro-code for LDA
            self.rf.ACC.write(self.rf.MDR.read())
            yield self._get_current_state(
                active_components={'MDR', 'ACC', 'CU'},
                active_buses={'MDR_ACC_BUS'}
            )
        
        elif opcode['name'] == 'ADD':
            # Simplified micro-code for ADD
            yield self._get_current_state(active_components={'ALU', 'ACC', 'MDR', 'CU'})
        
        elif opcode['name'] == 'STA':
            # Simplified micro-code for STA
            yield self._get_current_state(active_components={'ACC', 'MDR', 'MAR', 'RAM', 'CU'}, active_buses={'ADDR_BUS', 'DATA_BUS'})

        elif opcode['name'] == 'HALT':
            self.halted = True
            yield self._get_current_state(active_components={'CU', 'CPU_HALTED'})
        
        else:
            # For other instructions, just highlight the CU
            yield self._get_current_state(active_components={'CU'})