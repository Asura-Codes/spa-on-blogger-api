import os
import sys

from blogger_gui.ui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication


def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Blogger Gui")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
