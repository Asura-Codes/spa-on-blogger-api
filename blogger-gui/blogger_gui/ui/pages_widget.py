"""
Pages Widget Module

This module defines the widget for managing blog pages.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QMessageBox, QDialog, QLabel
)
from PyQt6.QtCore import Qt

from blogger_gui.ui.page_editor import PageEditor


class PagesWidget(QWidget):
    """Widget for managing blog pages"""
    
    def __init__(self, parent=None, api_client=None):
        super().__init__(parent)
        
        self.api_client = api_client
        self.current_blog_id = None
        self.pages = []
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the widget UI elements"""
        layout = QVBoxLayout(self)
        
        # Pages list
        self.page_list = QListWidget()
        self.page_list.currentRowChanged.connect(self._on_page_selected)
        layout.addWidget(QLabel("Pages:"))
        layout.addWidget(self.page_list)
        
        # Page actions
        page_actions_layout = QHBoxLayout()
        self.new_page_button = QPushButton("New Page")
        self.new_page_button.clicked.connect(self._create_new_page)
        self.edit_page_button = QPushButton("Edit Page")
        self.edit_page_button.clicked.connect(self._edit_page)
        self.delete_page_button = QPushButton("Delete Page")
        self.delete_page_button.clicked.connect(self._delete_page)
        
        page_actions_layout.addWidget(self.new_page_button)
        page_actions_layout.addWidget(self.edit_page_button)
        page_actions_layout.addWidget(self.delete_page_button)
        layout.addLayout(page_actions_layout)
        
        # Initially disable page actions until a blog is selected
        self._update_button_states()
    
    def set_blog_id(self, blog_id):
        """Set the current blog ID and load pages"""
        self.current_blog_id = blog_id
        if blog_id:
            self._load_pages()
        else:
            self.page_list.clear()
            self.pages = []
        
        self._update_button_states()
    
    def _load_pages(self):
        """Load pages for the selected blog"""
        if not self.current_blog_id:
            return
        
        self.page_list.clear()
        self.pages = self.api_client.get_pages(self.current_blog_id, max_results=20)
        
        if not self.pages:
            self.parent().statusBar().showMessage("No pages found for this blog")
            return
        
        for page in self.pages:
            self.page_list.addItem(page.get('title', 'Untitled Page'))
        
        # self.parent().statusBar().showMessage(f"Loaded {len(self.pages)} pages")
    
    def _on_page_selected(self, index):
        """Handle page selection"""
        self._update_button_states()
    
    def _update_button_states(self):
        """Update button states based on selections"""
        has_blog = self.current_blog_id is not None
        has_page = self.page_list.currentRow() >= 0 and len(self.pages) > 0
        
        self.new_page_button.setEnabled(has_blog)
        self.edit_page_button.setEnabled(has_blog and has_page)
        self.delete_page_button.setEnabled(has_blog and has_page)
    
    def _create_new_page(self):
        """Create a new page"""
        if not self.current_blog_id:
            return
        
        editor = PageEditor(self, self.api_client, self.current_blog_id)
        if editor.exec() == QDialog.DialogCode.Accepted:
            self._load_pages()
    
    def _edit_page(self):
        """Edit the selected page"""
        index = self.page_list.currentRow()
        if index < 0 or index >= len(self.pages):
            return
        
        page = self.pages[index]
        editor = PageEditor(self, self.api_client, self.current_blog_id, page)
        if editor.exec() == QDialog.DialogCode.Accepted:
            self._load_pages()
    
    def _delete_page(self):
        """Delete the selected page"""
        index = self.page_list.currentRow()
        if index < 0 or index >= len(self.pages):
            return
        
        page = self.pages[index]
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the page '{page.get('title')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.api_client.delete_page(self.current_blog_id, page.get('id')):
                self.parent().statusBar().showMessage("Page deleted successfully")
                self._load_pages()
            else:
                QMessageBox.critical(
                    self,
                    "Delete Failed",
                    "Failed to delete the page. Please try again."
                )
    
    def refresh(self):
        """Refresh the pages data"""
        if self.current_blog_id:
            self._load_pages()
