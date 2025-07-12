"""
Authentication Dialog Module

This module defines the dialog for setting up API authentication.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QDialogButtonBox
)
from PyQt6.QtCore import QSize
from pathlib import Path


class AuthDialog(QDialog):
    """Dialog for selecting API credentials file"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Blogger API Authentication")
        self.setMinimumSize(QSize(500, 150))
        
        self.credentials_path = ""
        
        layout = QVBoxLayout(self)
        
        # Instructions label
        instructions = QLabel(
            "Please select your credentials.json file from the Google Developer Console.\n"
            "If you don't have one, please create a project in the Google Developer Console,\n"
            "enable the Blogger API, and create OAuth credentials for a Desktop application."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # File selection
        file_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("No file selected")
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self._browse_credentials)
        
        file_layout.addWidget(QLabel("Credentials File:"))
        file_layout.addWidget(self.path_edit, 1)
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        # Default to credentials.json in the current directory if it exists
        default_path = Path("credentials.json")
        if default_path.exists():
            self.credentials_path = str(default_path.absolute())
            self.path_edit.setText(self.credentials_path)
    
    def _browse_credentials(self):
        """Open file browser to select credentials file"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Credentials File",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_name:
            self.credentials_path = file_name
            self.path_edit.setText(file_name)
    
    def accept(self):
        """Override accept to validate input"""
        if not self.credentials_path:
            return
        
        super().accept()
