"""
Main Window Module

This module defines the main application window for the Blogger Client.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QListWidget, QMessageBox, QDialog, QLabel, QSplitter
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction

from blogger_gui.api.blogger_api import BloggerApiClient
from blogger_gui.ui.auth_dialog import AuthDialog
from blogger_gui.ui.posts_widget import PostsWidget
from blogger_gui.ui.pages_widget import PagesWidget


class MainWindow(QMainWindow):
    """Main application window for the Blogger Client"""
    
    def __init__(self):
        super().__init__()
        
        self.api_client = BloggerApiClient()
        self.current_blog_id = None
        self.blogs = []
        
        self.setWindowTitle("Blogger Client")
        self.setMinimumSize(QSize(800, 600))
        
        self._create_actions()
        self._create_menu_bar()
        self._create_status_bar()
        self._create_central_widget()
        
        # Try to authenticate on startup
        self._authenticate()
    
    def _create_actions(self):
        """Create actions for menus"""
        self.auth_action = QAction("&Authenticate", self)
        self.auth_action.setStatusTip("Authenticate with Google Blogger API")
        self.auth_action.triggered.connect(self._authenticate)
        
        self.refresh_action = QAction("&Refresh", self)
        self.refresh_action.setStatusTip("Refresh blogs and posts")
        self.refresh_action.triggered.connect(self._refresh_data)
        
        self.exit_action = QAction("&Exit", self)
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.close)
    
    def _create_menu_bar(self):
        """Create the menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.auth_action)
        file_menu.addAction(self.refresh_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
    
    def _create_status_bar(self):
        """Create the status bar"""
        self.statusBar().showMessage("Ready")
    
    def _create_central_widget(self):
        """Create the central widget with blog list and content tabs"""
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # Create a splitter for the main areas
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Blog list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.blog_list = QListWidget()
        self.blog_list.currentRowChanged.connect(self._on_blog_selected)
        left_layout.addWidget(QLabel("Your Blogs:"))
        left_layout.addWidget(self.blog_list)
        
        # Right panel - Tab widget for Posts and Pages
        self.tab_widget = QTabWidget()
        
        # Create and add the posts widget
        self.posts_widget = PostsWidget(self, self.api_client)
        self.tab_widget.addTab(self.posts_widget, "Posts")
        
        # Create and add the pages widget
        self.pages_widget = PagesWidget(self, self.api_client)
        self.tab_widget.addTab(self.pages_widget, "Pages")
        
        # Add panels to splitter and set sizes
        splitter.addWidget(left_panel)
        splitter.addWidget(self.tab_widget)
        splitter.setSizes([200, 600])
        
        self.setCentralWidget(central_widget)
    
    def _authenticate(self):
        """Authenticate with the Blogger API"""
        auth_dialog = AuthDialog(self)
        if auth_dialog.exec() == QDialog.DialogCode.Accepted:
            self.api_client.credentials_file = auth_dialog.credentials_path
            
            if self.api_client.authenticate():
                self.statusBar().showMessage("Authentication successful")
                self._load_blogs()
            else:
                QMessageBox.critical(
                    self,
                    "Authentication Failed",
                    "Failed to authenticate with the Blogger API. Please check your credentials file."
                )
    
    def _load_blogs(self):
        """Load the user's blogs from the API"""
        self.blog_list.clear()
        
        # Reset the current blog ID and update the widgets
        self.current_blog_id = None
        self.posts_widget.set_blog_id(None)
        self.pages_widget.set_blog_id(None)
        
        self.blogs = self.api_client.get_blogs()
        
        if not self.blogs:
            self.statusBar().showMessage("No blogs found")
            return
        
        for blog in self.blogs:
            self.blog_list.addItem(blog.get('name', 'Unnamed Blog'))
        
        self.statusBar().showMessage(f"Loaded {len(self.blogs)} blogs")
    
    def _on_blog_selected(self, index):
        """Handle blog selection"""
        if index < 0 or index >= len(self.blogs):
            self.current_blog_id = None
            self.posts_widget.set_blog_id(None)
            self.pages_widget.set_blog_id(None)
            return
        
        self.current_blog_id = self.blogs[index].get('id')
        self.posts_widget.set_blog_id(self.current_blog_id)
        self.pages_widget.set_blog_id(self.current_blog_id)
        
        self.statusBar().showMessage(f"Selected blog: {self.blogs[index].get('name')}")
    
    def _refresh_data(self):
        """Refresh the blogs and posts data"""
        self._load_blogs()
        
        # If a blog is selected after reloading, refresh the content widgets
        if self.current_blog_id:
            self.posts_widget.refresh()
            self.pages_widget.refresh()
