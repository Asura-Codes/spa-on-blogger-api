"""
Post Editor Module

This module defines the dialog for creating and editing blog posts.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QCheckBox, QDialogButtonBox, 
    QPushButton, QMessageBox, QDateTimeEdit
)
from PyQt6.QtCore import QSize, QDateTime, Qt
from typing import Dict, Any, Optional, List
import datetime


class PostEditor(QDialog):
    """Dialog for creating and editing blog posts"""
    
    def __init__(self, parent=None, api_client=None, blog_id=None, post=None):
        super().__init__(parent)
        
        self.api_client = api_client
        self.blog_id = blog_id
        self.post = post
        self.edit_mode = post is not None
        
        self.setWindowTitle("Post Editor" if not self.edit_mode else "Edit Post")
        self.setMinimumSize(QSize(700, 500))
        
        self._create_ui()
        
        if self.edit_mode:
            self._populate_post_data()
    
    def _create_ui(self):
        """Create the dialog UI elements"""
        layout = QVBoxLayout(self)
        
        # Title
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Title:"))
        self.title_edit = QLineEdit()
        title_layout.addWidget(self.title_edit)
        layout.addLayout(title_layout)
        
        # Permalink URL
        permalink_layout = QHBoxLayout()
        permalink_layout.addWidget(QLabel("Permalink:"))
        self.permalink_edit = QLineEdit()
        self.permalink_edit.setPlaceholderText("Optional custom URL path")
        permalink_layout.addWidget(self.permalink_edit)
        layout.addLayout(permalink_layout)
        
        # Content (HTML editor)
        layout.addWidget(QLabel("Content (HTML):"))
        self.content_edit = QTextEdit()
        self.content_edit.setAcceptRichText(False)
        self.content_edit.setPlaceholderText("Enter HTML content here...")
        layout.addWidget(self.content_edit)
        
        # Labels/Tags
        labels_layout = QHBoxLayout()
        labels_layout.addWidget(QLabel("Labels (comma separated):"))
        self.labels_edit = QLineEdit()
        self.labels_edit.setPlaceholderText("label1, label2, label3")
        labels_layout.addWidget(self.labels_edit)
        layout.addLayout(labels_layout)
        
        # Publish date
        publish_date_layout = QHBoxLayout()
        publish_date_layout.addWidget(QLabel("Publish Date:"))
        self.publish_date_edit = QDateTimeEdit()
        self.publish_date_edit.setDateTime(QDateTime.currentDateTime())
        self.publish_date_edit.setCalendarPopup(True)
        self.publish_date_edit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        publish_date_layout.addWidget(self.publish_date_edit)
        
        # Checkbox to enable/disable custom publish date
        self.use_custom_date = QCheckBox("Use custom publish date")
        self.use_custom_date.setChecked(False)
        self.use_custom_date.toggled.connect(self._toggle_publish_date)
        publish_date_layout.addWidget(self.use_custom_date)
        
        layout.addLayout(publish_date_layout)
        
        # Reader comments
        self.allow_comments = QCheckBox("Allow reader comments")
        self.allow_comments.setChecked(True)
        layout.addWidget(self.allow_comments)
        
        # Draft checkbox (only for new posts)
        if not self.edit_mode:
            self.draft_checkbox = QCheckBox("Create as draft")
            self.draft_checkbox.setChecked(True)
            layout.addWidget(self.draft_checkbox)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save_post)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        # Initially disable publish date since custom date is unchecked by default
        self.publish_date_edit.setEnabled(False)
    
    def _populate_post_data(self):
        """Populate the form with existing post data"""
        if not self.post:
            return
        
        self.title_edit.setText(self.post.get('title', ''))
        self.content_edit.setPlainText(self.post.get('content', ''))
        
        # Populate permalink if available
        if 'url' in self.post:
            self.permalink_edit.setText(self.post.get('url', ''))
        
        # Populate labels if available
        labels = self.post.get('labels', [])
        if labels:
            self.labels_edit.setText(', '.join(labels))
        
        # Populate publish date if available
        if 'published' in self.post:
            try:
                # Format: 2025-06-23T10:00:00-07:00
                # Remove timezone part for simplicity
                date_str = self.post.get('published', '')
                if 'T' in date_str:
                    date_parts = date_str.split('T')
                    date_part = date_parts[0]
                    time_part = date_parts[1].split('-')[0].split('+')[0]  # Remove timezone
                    
                    dt = QDateTime.fromString(f"{date_part}T{time_part}", "yyyy-MM-ddThh:mm:ss")
                    if dt.isValid():
                        self.publish_date_edit.setDateTime(dt)
                        self.use_custom_date.setChecked(True)
                        self.publish_date_edit.setEnabled(True)
            except Exception:
                # If there's any issue parsing the date, just use current date
                pass
          # Set comment permissions
        settings = self.post.get('settings', {})
        comment_setting = settings.get('commentSetting', '')
        self.allow_comments.setChecked(comment_setting != 'BLOCK_COMMENTS')
    
    def _toggle_publish_date(self, enabled):
        """Enable or disable the publish date field based on the checkbox state"""
        self.publish_date_edit.setEnabled(enabled)
    
    def _parse_labels(self) -> List[str]:
        """Parse labels from comma-separated text input"""
        labels_text = self.labels_edit.text().strip()
        if not labels_text:
            return []
        
        # Split by comma and strip whitespace
        return [label.strip() for label in labels_text.split(',') if label.strip()]
    
    def _format_datetime_for_api(self, dt):
        """Format QDateTime to RFC 3339 format for the Blogger API"""
        # Format: 2025-06-23T10:00:00-07:00
        # We'll use local timezone for simplicity
        py_dt = dt.toPyDateTime()
        
        # Get timezone offset in hours
        utc_offset = datetime.datetime.now().astimezone().utcoffset()
        hours_offset = int(utc_offset.total_seconds() / 3600)
        
        # Format timezone string
        if hours_offset < 0:
            tz_str = f"-{abs(hours_offset):02d}:00"
        else:
            tz_str = f"+{hours_offset:02d}:00"
            
        # Format the final RFC 3339 string
        return py_dt.strftime("%Y-%m-%dT%H:%M:%S") + tz_str
    
    def _save_post(self):
        """Save the post to the Blogger API"""
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText().strip()
        labels = self._parse_labels()
        permalink = self.permalink_edit.text().strip()
        allow_comments = self.allow_comments.isChecked()
        
        # Get publish date if custom date is enabled
        publish_date = None
        if self.use_custom_date.isChecked():
            dt = self.publish_date_edit.dateTime()
            publish_date = self._format_datetime_for_api(dt)
        
        if not title:
            QMessageBox.warning(self, "Missing Information", "Please enter a title for the post.")
            return
        
        if not content:
            QMessageBox.warning(self, "Missing Information", "Please enter content for the post.")
            return
        
        try:
            if self.edit_mode:
                # Update existing post
                self.api_client.update_post(
                    self.blog_id,
                    self.post.get('id'),
                    title,
                    content,
                    labels,
                    publish_date,
                    permalink if permalink else None,
                    allow_comments
                )
                QMessageBox.information(self, "Success", "Post updated successfully.")
            else:
                # Create new post
                is_draft = self.draft_checkbox.isChecked()
                self.api_client.create_post(
                    self.blog_id,
                    title,
                    content,
                    labels,
                    is_draft,
                    publish_date,
                    permalink if permalink else None,
                    allow_comments
                )
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Post {'drafted' if is_draft else 'published'} successfully."
                )
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save post: {str(e)}")
