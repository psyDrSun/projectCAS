import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QToolBar, QAction
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon # Optional, for icons on buttons

from backend.core.computer import Computer
from .canvas_widget import CanvasWidget
from .left_panel import LeftPanel
from . import circuit_layout as layout

class MainWindow(QMainWindow):
    """
    The main application window. It orchestrates the UI components (LeftPanel, CanvasWidget)
    and manages the simulation flow by interacting with the backend computer model.
    """
    def __init__(self, computer: Computer):
        super().__init__()
        self.computer = computer
        self.micro_step_generator = None

        self.setWindowTitle("projectCAS - Turing Complete Visualizer")
        self.setGeometry(50, 50, 1400, 800)
        self.setStyleSheet(f"background-color: {layout.THEME['background']};")

        # --- Central Widget and Layout ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        # Use a horizontal layout to place the left panel and the canvas side-by-side
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- UI Components ---
        self.left_panel = LeftPanel()
        self.canvas = CanvasWidget()
        
        self.main_layout.addWidget(self.left_panel)
        self.main_layout.addWidget(self.canvas, 1) # The '1' gives the canvas more stretch space

        # --- Simulation Timer ---
        self.simulation_timer = QTimer(self)
        self.simulation_timer.timeout.connect(self.do_one_micro_step)
        
        self.create_toolbar()
        self.reset_computer() # Initialize the view on startup

    def create_toolbar(self):
        """Creates the top toolbar with simulation controls."""
        toolbar = self.addToolBar("Controls")
        toolbar.setMovable(False)
        toolbar.setStyleSheet(f"""
            QToolBar {{
                background-color: {layout.THEME['component_bg']};
                border-bottom: 1px solid {layout.THEME['component_border']};
                spacing: 10px;
                padding: 5px;
            }}
            QToolButton {{
                color: {layout.THEME['component_label']};
                font-weight: bold;
            }}
        """)
        
        # Run/Pause button (checkable)
        self.run_action = QAction("Run", self, checkable=True)
        self.run_action.toggled.connect(self.toggle_run)
        toolbar.addAction(self.run_action)

        # Single Step button
        step_action = QAction("Step", self)
        step_action.triggered.connect(self.do_one_micro_step)
        toolbar.addAction(step_action)

        # Reset button
        reset_action = QAction("Reset", self)
        reset_action.triggered.connect(self.reset_computer)
        toolbar.addAction(reset_action)

    def toggle_run(self, checked: bool):
        """Starts or stops the continuous simulation timer."""
        if checked:
            self.run_action.setText("Pause")
            self.simulation_timer.start(250) # Time in ms per micro-step
        else:
            self.run_action.setText("Run")
            self.simulation_timer.stop()

    def do_one_micro_step(self):
        """Executes a single micro-step and updates the entire UI."""
        if self.run_action.isChecked() and self.simulation_timer.isActive() == False:
             self.run_action.setChecked(False) # Stop if we reach the end in run mode
             return

        if self.micro_step_generator is None:
            # If there's no active generator, create one for the next macro instruction
            self.micro_step_generator = self.computer.get_micro_step_generator()
        
        try:
            # Fetch the next state from the backend's generator
            state = next(self.micro_step_generator)
            # Distribute the new state to all frontend components that need it
            self.canvas.update_state(state)
            self.left_panel.update_state(state)
        except StopIteration:
            # The current macro instruction is finished.
            self.micro_step_generator = None
            if self.run_action.isChecked(): # If in run mode, automatically start the next instruction
                 self.do_one_micro_step()
            else: # If in step mode, just stop and wait for the user
                 print("Macro-instruction finished. Ready for next step.")

    def reset_computer(self):
        """Resets the backend computer and the entire UI to its initial state."""
        if self.simulation_timer.isActive():
            self.run_action.setChecked(False) # This will also stop the timer
        
        self.computer.reset()
        # For demonstration, load the default program upon reset
        program_code = [0x44, 0x46, 0x98, 0x81, 0xF5, 0x0C, 0x00, 0x60]
        self.computer.load_program(program_code)
        
        self.micro_step_generator = None
        # Get the initial state from the reset computer
        initial_state = self.computer.cpu._get_current_state()
        # Update UI to reflect the initial state
        self.canvas.update_state(initial_state)
        self.left_panel.update_state(initial_state)
        print("Computer has been reset and program is loaded.")