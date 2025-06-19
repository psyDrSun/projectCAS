import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
                             QToolBar, QAction, QDockWidget, QTextEdit, QVBoxLayout,
                             QWidget, QPushButton, QPlainTextEdit, QGraphicsItem,
                             QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QPainterPath, QPen, QPainterPath, QFont

from .graphical_components import RamItem, CpuItem, Bus
from backend.core.computer import Computer

class MainWindow(QMainWindow):
    def __init__(self, computer: Computer):
        super().__init__()
        self.computer = computer
        self.setWindowTitle("projectCAS Visual Simulator")
        self.setGeometry(100, 100, 1600, 900)

        # Main graphics view
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1500, 1000)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.init_ui()
        self.load_computer_state()

    def init_ui(self):
        self.create_docks()
        self.create_toolbar()
        self.draw_computer_layout()

    def create_toolbar(self):
        toolbar = QToolBar("Controls")
        self.addToolBar(toolbar)

        load_action = QAction("Load Program", self)
        load_action.triggered.connect(self.load_program)
        toolbar.addAction(load_action)

        step_action = QAction("Step Macro", self)
        step_action.triggered.connect(self.step_macro)
        toolbar.addAction(step_action)

        reset_action = QAction("Reset", self)
        reset_action.triggered.connect(self.reset_computer)
        toolbar.addAction(reset_action)

    def create_docks(self):
        # Program Input Dock
        program_dock = QDockWidget("Program Code", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, program_dock)
        program_widget = QWidget()
        program_layout = QVBoxLayout()
        self.program_input = QPlainTextEdit()
        self.program_input.setFont(QFont("Courier New", 12))
        self.program_input.setPlaceholderText("Enter program hex codes, e.g., 44 46 98...")
        program_layout.addWidget(self.program_input)
        program_widget.setLayout(program_layout)
        program_dock.setWidget(program_widget)

        # Status Display Dock
        status_dock = QDockWidget("Status", self)
        self.addDockWidget(Qt.RightDockWidgetArea, status_dock)
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        self.status_display.setFont(QFont("Courier New", 11))
        status_dock.setWidget(self.status_display)

    def draw_computer_layout(self):
        """Draws the main components on the canvas."""
        self.cpu_item = CpuItem(500, 200)
        self.ram_item = RamItem(100, 100, 256) # 256 bytes RAM
        
        self.scene.addItem(self.cpu_item)
        self.scene.addItem(self.ram_item)

        # Draw Buses
        self.address_bus = Bus(self.cpu_item.get_port_pos('addr_out'), self.ram_item.get_port_pos('addr_in'))
        self.data_bus = Bus(self.cpu_item.get_port_pos('data_io'), self.ram_item.get_port_pos('data_io'), two_way=True)
        self.scene.addItem(self.address_bus)
        self.scene.addItem(self.data_bus)

    def load_computer_state(self):
        """Loads the current state from the backend and updates the UI."""
        self.ram_item.update_memory(self.computer.ram.memory)
        self.cpu_item.update_registers(self.computer.cpu.rf)
        self.status_display.setText(self.computer.get_full_status())

    def load_program(self):
        """Loads the program from the input box into the computer's memory."""
        try:
            self.reset_computer() # Reset before loading new program
            code_text = self.program_input.toPlainText().strip()
            if not code_text:
                program_code = [0x44, 0x46, 0x98, 0x81, 0xF5, 0x0C, 0x00, 0x60]
                self.program_input.setPlainText(' '.join(f'{b:02X}' for b in program_code))
            else:
                program_code = [int(hex_byte, 16) for hex_byte in code_text.split()]
            
            self.computer.load_program(program_code)
            self.load_computer_state()
            self.status_display.append("\nProgram loaded successfully.")
        except ValueError as e:
            self.status_display.append(f"\nError loading program: {e}")

    def step_macro(self):
        """Executes one macro instruction step."""
        if self.computer.cpu.halted:
            self.status_display.append("\n--- CPU HALTED ---")
            return

        pc_val = self.computer.cpu.rf.PC.read()
        self.computer.run_single_macro_step()
        self.load_computer_state()
        self.status_display.append(f"\n--- Executed Macro Instruction at PC=0x{pc_val:02X} ---")

    def reset_computer(self):
        """Resets the computer to its initial state."""
        self.computer.reset()
        self.load_computer_state()
        self.status_display.setText("--- Computer Reset ---")