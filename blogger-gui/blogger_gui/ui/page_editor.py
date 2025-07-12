"""
Page Editor Module

This module defines the dialog for creating and editing blog pages.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QCheckBox, QDialogButtonBox, 
    QPushButton, QMessageBox
)
from PyQt6.QtCore import QSize
from typing import Dict, Any, Optional


class PageEditor(QDialog):
    """Dialog for creating and editing blog pages"""
    
    def __init__(self, parent=None, api_client=None, blog_id=None, page=None):
        super().__init__(parent)
        
        self.api_client = api_client
        self.blog_id = blog_id
        self.page = page
        self.edit_mode = page is not None
        
        self.setWindowTitle("Page Editor" if not self.edit_mode else "Edit Page")
        self.setMinimumSize(QSize(700, 500))
        
        self._create_ui()
        
        if self.edit_mode:
            self._populate_page_data()
    
    def _create_ui(self):
        """Create the dialog UI elements"""
        layout = QVBoxLayout(self)
        
        # Title
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Title:"))
        self.title_edit = QLineEdit()
        title_layout.addWidget(self.title_edit)
        layout.addLayout(title_layout)
        
        # Content (HTML editor)
        layout.addWidget(QLabel("Content (HTML):"))
        self.content_edit = QTextEdit()
        self.content_edit.setAcceptRichText(False)
        self.content_edit.setPlaceholderText("Enter HTML content here...")
        layout.addWidget(self.content_edit)
        
        # Draft checkbox (only for new pages)
        if not self.edit_mode:
            self.draft_checkbox = QCheckBox("Create as draft")
            self.draft_checkbox.setChecked(True)
            layout.addWidget(self.draft_checkbox)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save_page)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _populate_page_data(self):
        """Populate the form with existing page data"""
        if not self.page:
            return
        
        self.title_edit.setText(self.page.get('title', ''))
        self.content_edit.setPlainText(self.page.get('content', ''))
    
    def _save_page(self):
        """Save the page to the Blogger API"""
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Missing Information", "Please enter a title for the page.")
            return
        
        if not content:
            QMessageBox.warning(self, "Missing Information", "Please enter content for the page.")
            return
        
        try:
            if self.edit_mode:
                # Update existing page
                self.api_client.update_page(
                    self.blog_id,
                    self.page.get('id'),
                    title,
                    content
                )
                QMessageBox.information(self, "Success", "Page updated successfully.")
            else:
                # Create new page
                is_draft = self.draft_checkbox.isChecked()
                self.api_client.create_page(
                    self.blog_id,
                    title,
                    content,
                    is_draft
                )
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Page {'drafted' if is_draft else 'published'} successfully."
                )
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save page: {str(e)}")
