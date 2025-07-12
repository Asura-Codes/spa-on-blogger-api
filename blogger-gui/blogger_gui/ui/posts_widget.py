"""
Posts Widget Module

This module defines the widget for managing blog posts.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QMessageBox, QDialog, QLabel, QSplitter
)
from PyQt6.QtCore import Qt

from blogger_gui.ui.post_editor import PostEditor


class PostsWidget(QWidget):
    """Widget for managing blog posts"""
    
    def __init__(self, parent=None, api_client=None):
        super().__init__(parent)
        
        self.api_client = api_client
        self.current_blog_id = None
        self.posts = []
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the widget UI elements"""
        layout = QVBoxLayout(self)
        
        # Posts list
        self.post_list = QListWidget()
        self.post_list.currentRowChanged.connect(self._on_post_selected)
        layout.addWidget(QLabel("Posts:"))
        layout.addWidget(self.post_list)
        
        # Post actions
        post_actions_layout = QHBoxLayout()
        self.new_post_button = QPushButton("New Post")
        self.new_post_button.clicked.connect(self._create_new_post)
        self.edit_post_button = QPushButton("Edit Post")
        self.edit_post_button.clicked.connect(self._edit_post)
        self.delete_post_button = QPushButton("Delete Post")
        self.delete_post_button.clicked.connect(self._delete_post)
        
        post_actions_layout.addWidget(self.new_post_button)
        post_actions_layout.addWidget(self.edit_post_button)
        post_actions_layout.addWidget(self.delete_post_button)
        layout.addLayout(post_actions_layout)
        
        # Initially disable post actions until a blog is selected
        self._update_button_states()
    
    def set_blog_id(self, blog_id):
        """Set the current blog ID and load posts"""
        self.current_blog_id = blog_id
        if blog_id:
            self._load_posts()
        else:
            self.post_list.clear()
            self.posts = []
        
        self._update_button_states()
    
    def _load_posts(self):
        """Load posts for the selected blog"""
        if not self.current_blog_id:
            return
        
        self.post_list.clear()
        self.posts = self.api_client.get_posts(self.current_blog_id, max_results=20)
        
        if not self.posts:
            self.parent().statusBar().showMessage("No posts found for this blog")
            return
        
        for post in self.posts:
            self.post_list.addItem(post.get('title', 'Untitled Post'))
        
        # self.parent().statusBar().showMessage(f"Loaded {len(self.posts)} posts")
    
    def _on_post_selected(self, index):
        """Handle post selection"""
        self._update_button_states()
    
    def _update_button_states(self):
        """Update button states based on selections"""
        has_blog = self.current_blog_id is not None
        has_post = self.post_list.currentRow() >= 0
        
        self.new_post_button.setEnabled(has_blog)
        self.edit_post_button.setEnabled(has_blog and has_post)
        self.delete_post_button.setEnabled(has_blog and has_post)
    
    def _create_new_post(self):
        """Open the post editor to create a new post"""
        if not self.current_blog_id:
            return
        
        editor = PostEditor(self, self.api_client, self.current_blog_id)
        if editor.exec() == QDialog.DialogCode.Accepted:
            self._load_posts()
    
    def _edit_post(self):
        """Open the post editor to edit the selected post"""
        index = self.post_list.currentRow()
        if index < 0 or index >= len(self.posts):
            return
        
        post = self.posts[index]
        editor = PostEditor(self, self.api_client, self.current_blog_id, post)
        if editor.exec() == QDialog.DialogCode.Accepted:
            self._load_posts()
    
    def _delete_post(self):
        """Delete the selected post"""
        index = self.post_list.currentRow()
        if index < 0 or index >= len(self.posts):
            return
        
        post = self.posts[index]
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the post '{post.get('title')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.api_client.delete_post(self.current_blog_id, post.get('id')):
                self.parent().statusBar().showMessage("Post deleted successfully")
                self._load_posts()
            else:
                QMessageBox.critical(
                    self,
                    "Delete Failed",
                    "Failed to delete the post. Please try again."
                )
    
    def refresh(self):
        """Refresh the posts data"""
        if self.current_blog_id:
            self._load_posts()
