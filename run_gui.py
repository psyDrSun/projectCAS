import sys
from PyQt5.QtWidgets import QApplication
from frontend.main_window import MainWindow
from backend.core.computer import Computer

def main():
    """
    GUI Application main function.
    """
    # 1. Create the backend computer instance
    computer = Computer()

    # 2. Create the PyQt Application
    app = QApplication(sys.argv)

    # 3. Create the Main Window and pass the computer instance to it
    window = MainWindow(computer)
    window.show()

    # 4. Execute the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()