from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from PyQt5.QtCore import Qt, QRect, QPoint

# We import our blueprint for all drawing instructions
from . import circuit_layout as layout

class CanvasWidget(QWidget):
    """
    The main drawing area for the computer architecture.
    It is entirely data-driven by the state dictionary passed to it.
    All drawing is done using QPainter on a strict grid system.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        # The 'state' dictionary holds all the real-time data from the backend
        self.state = {} 

    def update_state(self, new_state: dict):
        """
        Public method to receive the latest state from the backend.
        Calling this triggers a repaint of the widget.
        """
        self.state = new_state
        self.update() # This schedules a paintEvent

    def paintEvent(self, event):
        """
        Handles all the drawing. It's called automatically when self.update() is invoked.
        The drawing process is executed in a specific order to ensure correct layering.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Draw the dark background
        painter.fillRect(self.rect(), QColor(layout.THEME["background"]))

        # 2. Draw all the wires/buses first, so they appear underneath the components
        self._draw_wires(painter)

        # 3. Draw all the component boxes on top of the wires
        self._draw_components(painter)

    def _draw_components(self, painter: QPainter):
        """Draws all the component rectangles and their labels."""
        active_comps = self.state.get("active_components", set())
        font = QFont(layout.THEME["font"], layout.THEME["font_size"], QFont.Bold)
        
        for name, spec in layout.COMPONENTS.items():
            is_active = name in active_comps
            
            # Convert grid units from the layout file to actual pixel coordinates
            px_rect = QRect(
                spec["grid_pos"][0] * layout.GRID_SIZE,
                spec["grid_pos"][1] * layout.GRID_SIZE,
                spec["grid_size"][0] * layout.GRID_SIZE,
                spec["grid_size"][1] * layout.GRID_SIZE
            )
            
            # Determine border color based on activation state
            border_color = QColor(layout.THEME["component_border_active"]) if is_active else QColor(layout.THEME["component_border"])
            
            pen = QPen(border_color, 1.5)
            painter.setPen(pen)
            painter.setBrush(QColor(layout.THEME["component_bg"]))
            painter.drawRect(px_rect)
            
            # Draw the text label inside the component
            painter.setPen(QColor(layout.THEME["component_label"]))
            painter.setFont(font)
            painter.drawText(px_rect, Qt.AlignCenter, spec["label"])

    def _draw_wires(self, painter: QPainter):
        """Draws all the wires/buses based on the paths defined in the layout."""
        active_buses = self.state.get("active_buses", set())

        for name, points in layout.WIRES.items():
            is_active = name in active_buses
            
            # Determine wire color and thickness based on activation state
            if is_active:
                color = QColor(layout.THEME["wire_colors"].get(name, layout.THEME["wire_colors"]["DEFAULT"]))
                thickness = 2.5
            else:
                color = QColor(layout.THEME["wire_idle"])
                thickness = 1.5
            
            # --- FIX ---
            # The QPen constructor does not accept a 'joinStyle' keyword argument.
            # We must create the pen first, and then set its join style.
            pen = QPen(color, thickness)
            pen.setJoinStyle(Qt.MiterJoin)
            # -----------
            
            painter.setPen(pen)
            
            # Build a QPainterPath from the list of grid points
            path = QPainterPath()
            start_point = QPoint(
                points[0][0] * layout.GRID_SIZE,
                points[0][1] * layout.GRID_SIZE
            )
            path.moveTo(start_point)
            
            for i in range(1, len(points)):
                next_point = QPoint(
                    points[i][0] * layout.GRID_SIZE,
                    points[i][1] * layout.GRID_SIZE
                )
                path.lineTo(next_point)
            
            # Draw the entire path at once
            painter.drawPath(path)