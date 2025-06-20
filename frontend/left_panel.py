from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

# We import our blueprint for all styling instructions
from . import circuit_layout as layout

class InfoLabel(QWidget):
    """A custom widget to display a single piece of information (e.g., a register)."""
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        # --- FIX ---
        # Renamed the local variable from 'layout' to 'vbox' to avoid shadowing
        # the imported 'circuit_layout as layout' module.
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(5, 2, 5, 2)
        vbox.setSpacing(0)
        # -----------

        self.name_label = QLabel(name)
        self.name_label.setFont(QFont(layout.THEME["font"], layout.THEME["font_size"] - 1, QFont.Normal))
        self.name_label.setStyleSheet(f"color: {QColor(layout.THEME['component_label']).name()};")
        
        self.value_label = QLabel("0x00")
        self.value_label.setFont(QFont(layout.THEME["font"], layout.THEME["font_size"] + 4, QFont.Bold))
        self.value_label.setStyleSheet(f"color: {QColor(layout.THEME['wire_colors']['DEFAULT']).name()}; padding-left: 5px;")

        vbox.addWidget(self.name_label)
        vbox.addWidget(self.value_label)

    def set_value(self, value: int):
        # Special case for HALTED flag to show text instead of hex
        if self.name_label.text() == "HALTED":
             status_text = "YES" if value == 1 else "NO"
             self.value_label.setText(status_text)
        else:
             self.value_label.setText(f"0x{value:02X}")

class LeftPanel(QWidget):
    """
    The left-side information panel.
    It displays real-time data like register values and system status.
    It is data-driven by the state dictionary passed to its update_state method.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet(f"background-color: {layout.THEME['background']};")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.info_widgets = {}

        self._create_section("REGISTERS", ["PC", "ACC", "IR", "MAR", "MDR", "FLAG"])
        self._create_section("STATUS", ["HALTED"])

    def _create_section(self, title: str, item_names: list):
        """Helper method to create a titled section with info labels."""
        title_label = QLabel(title)
        title_label.setFont(QFont(layout.THEME["font"], layout.THEME["font_size"] + 2, QFont.Bold))
        title_label.setStyleSheet(f"color: {layout.THEME['component_label']}; margin-bottom: 5px;")
        self.main_layout.addWidget(title_label)

        for name in item_names:
            info_widget = InfoLabel(name)
            self.info_widgets[name] = info_widget
            self.main_layout.addWidget(info_widget)
        
        # Add a separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"border-top: 1px solid {layout.THEME['component_border']};")
        self.main_layout.addWidget(line)

    def update_state(self, new_state: dict):
        """
        Public method to receive the latest state and update all display widgets.
        """
        # Update register values
        if "registers" in new_state:
            for name, value in new_state["registers"].items():
                if name in self.info_widgets:
                    self.info_widgets[name].set_value(value)
        
        # Update status flags
        if "halted" in new_state:
            halted_status = 1 if new_state["halted"] else 0
            if "HALTED" in self.info_widgets:
                self.info_widgets["HALTED"].set_value(halted_status)