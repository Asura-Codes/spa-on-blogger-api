"""
Blogger API Client Module

This module handles authentication and API requests to the Blogger API.
"""

import os
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Any

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource


class BloggerApiClient:
    """Client for interacting with the Blogger API v3"""
    
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/blogger']
    API_SERVICE_NAME = 'blogger'
    API_VERSION = 'v3'
    
    def __init__(self, credentials_file: str = 'credentials.json'):
        """
        Initialize the Blogger API client
        
        Args:
            credentials_file: Path to the credentials JSON file from Google Developer Console
        """
        self.credentials_file = credentials_file
        self.service = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with the Blogger API using OAuth2
        
        Returns:
            bool: True if authentication was successful
        """
        creds = None
        
        # The file token.pickle stores the user's access and refresh tokens
        token_path = Path('token.pickle')
        if token_path.exists():
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
                
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not Path(self.credentials_file).exists():
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
                
        self.service = build(self.API_SERVICE_NAME, self.API_VERSION, credentials=creds)
        return True
        
    def get_blogs(self) -> List[Dict[str, Any]]:
        """
        Get the list of blogs for the authenticated user
        
        Returns:
            List of blog information dictionaries
        """
        if not self.service:
            if not self.authenticate():
                return []
            
        blogs = self.service.blogs().listByUser(userId='self').execute()
        return blogs.get('items', [])
        
    def get_posts(self, blog_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get posts from a specific blog
        
        Args:
            blog_id: The ID of the blog to get posts from
            max_results: Maximum number of posts to return
            
        Returns:
            List of post information dictionaries
        """
        if not self.service:
            if not self.authenticate():
                return []
            
        posts = self.service.posts().list(
            blogId=blog_id,
            maxResults=max_results
        ).execute()
        
        return posts.get('items', [])
        
    def create_post(self, blog_id: str, title: str, content: str, 
                    labels: Optional[List[str]] = None, is_draft: bool = True,
                    publish_date: Optional[str] = None, url: Optional[str] = None,
                    allow_comments: bool = True) -> Dict[str, Any]:
        """
        Create a new blog post
        
        Args:
            blog_id: The ID of the blog to create the post in
            title: The title of the post
            content: The HTML content of the post
            labels: List of labels/tags for the post
            is_draft: Whether the post should be created as a draft (True) or published (False)
            publish_date: RFC 3339 formatted date for post publication (e.g. '2025-06-23T12:00:00-08:00')
            url: Custom permalink URL path for the post
            allow_comments: Whether to allow reader comments on the post
            
        Returns:
            The created post information dictionary
        """
        if not self.service:
            if not self.authenticate():
                return {}
            
        post_body = {
            'kind': 'blogger#post',
            'title': title,
            'content': content,
        }
        
        if labels:
            post_body['labels'] = labels
            
        status = 'DRAFT' if is_draft else 'LIVE'
        post_body['status'] = status
          # Set custom publish date if provided
        if publish_date:
            post_body['published'] = publish_date
            
        # Set custom permalink URL if provided
        if url:
            post_body['url'] = url
            
        # Set comment settings
        if not allow_comments:
            post_body['settings'] = {'commentSetting': 'BLOCK_COMMENTS'}
        
        post = self.service.posts().insert(
            blogId=blog_id,
            body=post_body
        ).execute()
        
        return post
        
    def update_post(self, blog_id: str, post_id: str, title: str, 
                    content: str, labels: Optional[List[str]] = None,
                    publish_date: Optional[str] = None, url: Optional[str] = None,
                    allow_comments: Optional[bool] = None) -> Dict[str, Any]:
        """
        Update an existing blog post
        
        Args:
            blog_id: The ID of the blog containing the post
            post_id: The ID of the post to update
            title: The updated title
            content: The updated HTML content
            labels: Updated list of labels/tags
            publish_date: RFC 3339 formatted date for post publication (e.g. '2025-06-23T12:00:00-08:00')
            url: Custom permalink URL path for the post
            allow_comments: Whether to allow reader comments on the post
            
        Returns:
            The updated post information dictionary
        """
        if not self.service:
            if not self.authenticate():
                return {}
            
        post_body = {
            'kind': 'blogger#post',
            'title': title,
            'content': content,
        }
        
        if labels:
            post_body['labels'] = labels
            
        # Set custom publish date if provided
        if publish_date:
            post_body['published'] = publish_date
              # Set custom permalink URL if provided
        if url:
            post_body['url'] = url
            
        # Set comment settings if provided
        if allow_comments is not None and not allow_comments:
            post_body['settings'] = {'commentSetting': 'BLOCK_COMMENTS'}
            
        post = self.service.posts().update(
            blogId=blog_id,
            postId=post_id,
            body=post_body
        ).execute()
        
        return post
        
    def delete_post(self, blog_id: str, post_id: str) -> bool:
        """
        Delete a blog post
        
        Args:
            blog_id: The ID of the blog containing the post
            post_id: The ID of the post to delete
            
        Returns:
            True if the deletion was successful
        """
        if not self.service:
            if not self.authenticate():
                return False
            
        try:
            self.service.posts().delete(blogId=blog_id, postId=post_id).execute()
            return True
        except Exception:
            return False
        
    def get_pages(self, blog_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get pages from a specific blog
        
        Args:
            blog_id: The ID of the blog to get pages from
            max_results: Maximum number of pages to return
            
        Returns:
            List of page information dictionaries
        """
        if not self.service:
            if not self.authenticate():
                return []
            
        pages = self.service.pages().list(
            blogId=blog_id,
            maxResults=max_results
        ).execute()
        
        return pages.get('items', [])
        
    def get_page(self, blog_id: str, page_id: str) -> Dict[str, Any]:
        """
        Get a specific page
        
        Args:
            blog_id: The ID of the blog containing the page
            page_id: The ID of the page to retrieve
            
        Returns:
            The page information dictionary
        """
        if not self.service:
            if not self.authenticate():
                return {}
            
        try:
            page = self.service.pages().get(
                blogId=blog_id,
                pageId=page_id
            ).execute()
            return page
        except Exception:
            return {}
        
    def create_page(self, blog_id: str, title: str, content: str, 
                   is_draft: bool = True) -> Dict[str, Any]:
        """
        Create a new blog page
        
        Args:
            blog_id: The ID of the blog to create the page in
            title: The title of the page
            content: The HTML content of the page
            is_draft: Whether the page should be created as a draft (True) or published (False)
            
        Returns:
            The created page information dictionary
        """
        if not self.service:
            if not self.authenticate():
                return {}
            
        page_body = {
            'kind': 'blogger#page',
            'title': title,
            'content': content,
        }
            
        status = 'DRAFT' if is_draft else 'LIVE'
        page_body['status'] = status
        
        page = self.service.pages().insert(
            blogId=blog_id,
            body=page_body
        ).execute()
        
        return page
        
    def update_page(self, blog_id: str, page_id: str, title: str, 
                   content: str) -> Dict[str, Any]:
        """
        Update an existing blog page
        
        Args:
            blog_id: The ID of the blog containing the page
            page_id: The ID of the page to update
            title: The updated title
            content: The updated HTML content
            
        Returns:
            The updated page information dictionary
        """
        if not self.service:
            if not self.authenticate():
                return {}
            
        page_body = {
            'kind': 'blogger#page',
            'title': title,
            'content': content,
        }
            
        page = self.service.pages().update(
            blogId=blog_id,
            pageId=page_id,
            body=page_body
        ).execute()
        
        return page
        
    def delete_page(self, blog_id: str, page_id: str) -> bool:
        """
        Delete a blog page
        
        Args:
            blog_id: The ID of the blog containing the page
            page_id: The ID of the page to delete
            
        Returns:
            True if the deletion was successful
        """
        if not self.service:
            if not self.authenticate():
                return False
            
        try:
            self.service.pages().delete(blogId=blog_id, pageId=page_id).execute()
            return True
        except Exception:
            return False
