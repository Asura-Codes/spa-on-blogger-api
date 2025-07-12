"""
Tests for the Blogger API client
"""

import os
import pytest
from unittest.mock import MagicMock, patch
from blogger_gui.api.blogger_api import BloggerApiClient


class TestBloggerApiClient:
    """Test class for BloggerApiClient"""
    
    def test_init(self):
        """Test initialization of the client"""
        client = BloggerApiClient()
        assert client.credentials_file == 'credentials.json'
        assert client.service is None
    
    @patch('blogger_gui.api.blogger_api.build')
    @patch('blogger_gui.api.blogger_api.InstalledAppFlow')
    @patch('blogger_gui.api.blogger_api.Path.exists')
    def test_authenticate_new_creds(self, mock_exists, mock_flow, mock_build):
        """Test authentication with new credentials"""
        # Setup mocks
        mock_exists.return_value = True
        mock_flow_instance = MagicMock()
        mock_flow.from_client_secrets_file.return_value = mock_flow_instance
        mock_creds = MagicMock()
        mock_flow_instance.run_local_server.return_value = mock_creds
        
        # Create client and authenticate
        client = BloggerApiClient()
        result = client.authenticate()
        
        # Assertions
        assert result is True
        mock_flow.from_client_secrets_file.assert_called_once_with(
            client.credentials_file, client.SCOPES)
        mock_build.assert_called_once_with(
            client.API_SERVICE_NAME, client.API_VERSION, credentials=mock_creds)
    
    @patch('blogger_gui.api.blogger_api.build')
    def test_get_blogs(self, mock_build):
        """Test getting blogs"""
        # Setup mocks
        mock_service = MagicMock()
        mock_blogs = MagicMock()
        mock_blogs.listByUser().execute.return_value = {'items': [{'id': '123', 'name': 'Test Blog'}]}
        mock_service.blogs.return_value = mock_blogs
        mock_build.return_value = mock_service
        
        # Create client with authentication mocked
        client = BloggerApiClient()
        client.authenticate = MagicMock(return_value=True)
        client.service = mock_service
        
        # Get blogs
        blogs = client.get_blogs()
        
        # Assertions
        assert len(blogs) == 1
        assert blogs[0]['id'] == '123'
        assert blogs[0]['name'] == 'Test Blog'
        mock_blogs.listByUser.assert_called_once_with(userId='self')
    
    @patch('blogger_gui.api.blogger_api.build')
    def test_get_posts(self, mock_build):
        """Test getting posts"""
        # Setup mocks
        mock_service = MagicMock()
        mock_posts = MagicMock()
        mock_posts.list().execute.return_value = {
            'items': [{'id': 'post1', 'title': 'Test Post'}]
        }
        mock_service.posts.return_value = mock_posts
        mock_build.return_value = mock_service
        
        # Create client with authentication mocked
        client = BloggerApiClient()
        client.authenticate = MagicMock(return_value=True)
        client.service = mock_service
        
        # Get posts
        posts = client.get_posts('blog123', max_results=5)
        
        # Assertions
        assert len(posts) == 1
        assert posts[0]['id'] == 'post1'
        assert posts[0]['title'] == 'Test Post'
        mock_posts.list.assert_called_once_with(blogId='blog123', maxResults=5)
