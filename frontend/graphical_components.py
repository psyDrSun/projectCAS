# ````python name=frontend/graphical_components.py
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsPathItem, QGraphicsPolygonItem
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QColor, QBrush, QPen, QPainterPath, QFont

# --- Helper Functions ---
def create_box(parent, x, y, w, h, name, color=QColor("lightblue")):
    box = QGraphicsRectItem(x, y, w, h, parent)
    box.setBrush(color)
    text = QGraphicsTextItem(name, parent)
    text.setPos(x + w/2 - text.boundingRect().width()/2, y + h/2 - text.boundingRect().height()/2)
    return box, text

# --- Main Component Items ---

class RamItem(QGraphicsRectItem):
    def __init__(self, x, y, size, parent=None):
        super().__init__(x, y, 150, 300, parent)
        self.setBrush(QColor("lightgreen"))
        
        self.title = QGraphicsTextItem("RAM", self)
        self.title.setPos(x + 75 - self.title.boundingRect().width()/2, y + 5)
        
        self.mem_display = QGraphicsTextItem(self)
        self.mem_display.setPos(x + 10, y + 30)
        self.mem_display.setFont(QFont("Courier New", 9))
        
        # Ports for connecting buses
        self.ports = {
            'addr_in': QPointF(x, y + 50),
            'data_io': QPointF(x, y + 100)
        }

    def update_memory(self, memory_array):
        # Display first 16 bytes for simplicity
        display_text = ""
        for i in range(16):
            display_text += f"0x{i:02X}: {memory_array[i]:02X}\n"
        self.mem_display.setPlainText(display_text)
        
    def get_port_pos(self, name):
        return self.mapToScene(self.ports.get(name, QPointF(0, 0)))

    def highlight_address(self, address):
        # Later: visually indicate which memory cell is being accessed
        pass

    def unhighlight_all(self):
        pass


class RegisterItem(QGraphicsRectItem):
    def __init__(self, x, y, name, parent=None):
        super().__init__(x, y, 80, 40, parent)
        self.setBrush(QColor("ivory"))
        self.setPen(QPen(Qt.black, 1))
        
        self.name_text = QGraphicsTextItem(name, self)
        self.name_text.setPos(x + 5, y + 1)
        
        self.value_text = QGraphicsTextItem("0x00", self)
        self.value_text.setPos(x + 20, y + 15)
        self.value_text.setFont(QFont("Courier New", 12, QFont.Bold))

    def update_value(self, value):
        self.value_text.setPlainText(f"0x{value:02X}")
        
    def highlight(self):
        self.setBrush(QColor("gold"))

    def unhighlight(self):
        self.setBrush(QColor("ivory"))


class CpuItem(QGraphicsRectItem):
    def __init__(self, x, y, parent=None):
        super().__init__(x, y, 300, 400, parent)
        self.setBrush(QColor(240, 240, 240)) # Light grey
        self.setPen(QPen(Qt.darkGray, 2))

        self.title = QGraphicsTextItem("CPU", self)
        self.title.setPos(x + 150 - self.title.boundingRect().width()/2, y + 5)

        # Internal components
        self.alu_box, _ = create_box(self, x+20, y+50, 100, 80, "ALU")
        self.cu_box, _ = create_box(self, x+180, y+50, 100, 80, "Control Unit")

        # Registers
        self.registers = {
            'PC': RegisterItem(x+30, y+150, "PC", self),
            'ACC': RegisterItem(x+30, y+200, "ACC", self),
            'IR': RegisterItem(x+30, y+250, "IR", self),
            'MAR': RegisterItem(x+170, y+150, "MAR", self),
            'MDR': RegisterItem(x+170, y+200, "MDR", self),
            'FLAG': RegisterItem(x+170, y+250, "FLAG", self)
        }
        
        # Ports for connecting buses
        self.ports = {
            'addr_out': QPointF(x + 300, y + 100),
            'data_io': QPointF(x + 300, y + 200)
        }

    def get_port_pos(self, name):
        return self.mapToScene(self.ports.get(name, QPointF(0, 0)))

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
    def __init__(self, start_pos, end_pos, two_way=False):
        path = QPainterPath(start_pos)
        path.lineTo(end_pos)
        super().__init__(path)
        
        self.setPen(QPen(Qt.black, 2))
        self.two_way = two_way
        # Add arrows if desired
        
    def pulse(self, duration=500):
        # Simple animation placeholder
        self.setPen(QPen(Qt.red, 4))
        # Need a QTimer to reset the pen color after duration