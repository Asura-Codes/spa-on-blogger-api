# Blogger Client

A desktop client for managing Google Blogger blogs using Python 3 and PyQt6.

## Features

- OAuth authentication with Google Blogger API
- Browse and manage multiple blogs
- View, create, edit, and delete blog posts
- Rich text editing for post content
- Tag/label management for posts

## Requirements

- Python 3.7+
- PyQt6
- Google API Python Client
- Google Auth OAuthlib

## Installation

1. Clone this repository
2. Run the setup script to create a virtual environment:
   ```
   .\setup.ps1
   ```
3. Activate the virtual environment:
   - Windows: `. .venv\Scripts\Activate.ps1`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

   Alternatively, you can use the VS Code task "Install Requirements" after activating the virtual environment.

## Setting Up Google API Access

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Blogger API for your project
4. Create OAuth 2.0 credentials:
   - Application type: Desktop app
   - Download the credentials JSON file
   - Save it as `credentials.json` in the project directory

## Usage

Run the application:

```
# From the activated virtual environment
python -m blogger_gui
```

Alternatively, you can use the VS Code task "Run Blogger Gui Module" to start the application.

On first run, you'll need to:
1. Select your credentials file
2. Authenticate with your Google account
3. Grant permission to access your Blogger blogs

## Development

This project uses VS Code tasks for development and debugging:

- **Run Blogger Gui Module**: Executes the application
- **Run Tests**: Runs the pytest test suite with verbose output
- **Install Requirements**: Installs all dependencies from requirements.txt
- **Build Blogger Gui with PyInstaller**: Creates a standalone executable

To run the tests:

```
# From the activated virtual environment
python -m pytest tests -v
```

Alternatively, use the VS Code task "Run Tests".

## License

MIT License
