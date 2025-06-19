from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, 
                             QGraphicsPathItem, QGraphicsEllipseItem, QGraphicsLineItem)
from PyQt5.QtCore import QRectF, Qt, QPointF, QTimer
from PyQt5.QtGui import QColor, QBrush, QPen, QPainterPath, QFont

# --- Constants for Styling ---
PIN_RADIUS = 6
PORT_COLOR = QColor("#d35400") # Orange
BUS_COLOR = QColor("#2980b9") # Blue
BUS_PULSE_COLOR = QColor("#f1c40f") # Yellow
COMPONENT_BG_COLOR = QColor("#ecf0f1") # Light Grey
COMPONENT_BORDER_COLOR = QColor("#7f8c8d") # Grey
CPU_BG_COLOR = QColor(240, 240, 240, 200)

class Port(QGraphicsEllipseItem):
    """A small circle representing an input/output pin on a component."""
    def __init__(self, parent, is_output=False):
        super().__init__(-PIN_RADIUS, -PIN_RADIUS, PIN_RADIUS*2, PIN_RADIUS*2, parent)
        self.setBrush(PORT_COLOR)
        self.setPen(QPen(Qt.black, 1.5))

class RegisterItem(QGraphicsRectItem):
    """A detailed visual representation of a single register."""
    def __init__(self, name, parent=None):
        super().__init__(0, 0, 100, 45, parent)
        self.setBrush(COMPONENT_BG_COLOR)
        self.setPen(QPen(COMPONENT_BORDER_COLOR, 1.5))
        self.setToolTip(f"Register {name}")

        self.name_text = QGraphicsTextItem(name, self)
        self.name_text.setPos(5, 1)
        
        self.value_text = QGraphicsTextItem("0x00", self)
        self.value_text.setPos(25, 15)
        self.value_text.setFont(QFont("Courier New", 13, QFont.Bold))

    def update_value(self, value):
        self.value_text.setPlainText(f"0x{value:02X}")
        
    def highlight(self, color=QColor("gold")):
        self.setBrush(color)

    def unhighlight(self):
        self.setBrush(COMPONENT_BG_COLOR)

class RamItem(QGraphicsRectItem):
    """A Logisim-style RAM component."""
    def __init__(self, x, y, size, parent=None):
        super().__init__(x, y, 180, 350, parent)
        self.setBrush(COMPONENT_BG_COLOR)
        self.setPen(QPen(COMPONENT_BORDER_COLOR, 2))
        
        self.title = QGraphicsTextItem("RAM", self)
        self.title.setFont(QFont("Arial", 14, QFont.Bold))
        self.title.setPos(x + self.rect().width()/2 - self.title.boundingRect().width()/2, y + 5)
        
        self.mem_display = QGraphicsTextItem(self)
        self.mem_display.setPos(x + 15, y + 40)
        self.mem_display.setFont(QFont("Courier New", 10))
        
        self.ports = {
            'addr_in': Port(self),
            'data_io': Port(self),
        }
        self.ports['addr_in'].setPos(x, y + 80)
        self.ports['data_io'].setPos(x, y + 160)

    def update_memory(self, memory_array):
        # Display first 16 bytes
        display_text = ""
        for i in range(16):
            display_text += f"0x{i:02X}: <b style='color:blue;'>{memory_array[i]:02X}</b>\n"
        self.mem_display.setHtml(display_text)
        
    def get_port_pos(self, name):
        return self.ports.get(name).scenePos()

class AluItem(QGraphicsPathItem):
    """A trapezoidal ALU symbol."""
    def __init__(self, parent=None):
        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(120, 0)
        path.lineTo(100, 100)
        path.lineTo(20, 100)
        path.closeSubpath()
        super().__init__(path, parent)
        
        self.setBrush(COMPONENT_BG_COLOR)
        self.setPen(QPen(COMPONENT_BORDER_COLOR, 1.5))
        
        self.title = QGraphicsTextItem("ALU", self)
        self.title.setPos(self.boundingRect().width()/2 - self.title.boundingRect().width()/2, 40)

class CpuItem(QGraphicsRectItem):
    """A detailed CPU container showing internal components."""
    def __init__(self, x, y, parent=None):
        super().__init__(x, y, 450, 400, parent)
        self.setBrush(CPU_BG_COLOR)
        self.setPen(QPen(Qt.darkGray, 2, Qt.DashLine))

        self.title = QGraphicsTextItem("CPU", self)
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.title.setPos(x + self.rect().width()/2 - self.title.boundingRect().width()/2, y + 5)

        # --- Internal Components ---
        self.alu = AluItem(self)
        self.alu.setPos(x + 30, y + 80)

        self.cu = QGraphicsRectItem(x + 250, y + 80, 150, 100, self)
        self.cu.setBrush(COMPONENT_BG_COLOR)
        self.cu.setPen(QPen(COMPONENT_BORDER_COLOR, 1.5))
        cu_text = QGraphicsTextItem("Control Unit", self.cu)
        cu_text.setPos(self.cu.rect().center().x() - cu_text.boundingRect().width()/2, 
                       self.cu.rect().center().y() - cu_text.boundingRect().height()/2)

        # --- Register File ---
        reg_file_box = QGraphicsRectItem(x + 20, y + 220, 410, 160, self)
        reg_file_box.setBrush(QColor(220, 220, 220, 150))
        reg_file_box.setPen(QPen(Qt.darkGray, 1, Qt.DotLine))
        
        self.registers = {
            'PC': RegisterItem("PC", self), 'ACC': RegisterItem("ACC", self), 'IR': RegisterItem("IR", self),
            'MAR': RegisterItem("MAR", self), 'MDR': RegisterItem("MDR", self), 'FLAG': RegisterItem("FLAG", self)
        }
        self.registers['PC'].setPos(x + 40, y + 240)
        self.registers['MAR'].setPos(x + 40, y + 310)
        self.registers['ACC'].setPos(x + 180, y + 240)
        self.registers['MDR'].setPos(x + 180, y + 310)
        self.registers['IR'].setPos(x + 320, y + 240)
        self.registers['FLAG'].setPos(x + 320, y + 310)

        # --- External Ports ---
        self.ports = {
            'addr_out': Port(self), 'data_io': Port(self)
        }
        self.ports['addr_out'].setPos(x + self.rect().width(), y + 100)
        self.ports['data_io'].setPos(x + self.rect().width(), y + 200)

    def get_port_pos(self, name):
        return self.ports.get(name).scenePos()

    def update_registers(self, register_file):
        self.registers['PC'].update_value(register_file.PC.read())
        self.registers['ACC'].update_value(register_file.R0.read())
        self.registers['IR'].update_value(register_file.IR.read())
        self.registers['MAR'].update_value(register_file.AR.read())
        self.registers['MDR'].update_value(register_file.DR2.read())
        self.registers['FLAG'].update_value(register_file.FLAGS.read())
            
    def get_register_item(self, name):
        return self.registers.get(name)

class Bus(QGraphicsPathItem):
    """A bus that uses orthogonal lines and can be pulsed."""
    def __init__(self, start_pos, end_pos, two_way=False):
        super().__init__()
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.pen = QPen(BUS_COLOR, 3)
        self.setPen(self.pen)
        self.draw_path()

    def draw_path(self):
        path = QPainterPath(self.start_pos)
        # Create a simple orthogonal path (horizontal then vertical)
        mid_x = self.end_pos.x()
        path.lineTo(mid_x, self.start_pos.y())
        path.lineTo(self.end_pos)
        self.setPath(path)
        
    def pulse(self, duration=300):
        self.setPen(QPen(BUS_PULSE_COLOR, 4.5))
        QTimer.singleShot(duration, self.reset_pen)

    def reset_pen(self):
        self.setPen(self.pen)