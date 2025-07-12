# PyPI Publishing Guide for Blogger CLI

This document explains how to build and publish the Blogger CLI package to PyPI.

## Prerequisites

Before publishing to PyPI, ensure you have:

1. An account on [PyPI](https://pypi.org/) or [TestPyPI](https://test.pypi.org/)
2. The latest versions of build and twine:
   ```
   python -m pip install build twine --upgrade
   ```

## Building and Publishing Process

### Using VS Code Tasks

We've set up VS Code tasks to simplify the process:

1. **Build for PyPI**: Creates the distribution packages
   - Press `Ctrl+Shift+P`, select "Tasks: Run Task", then "Build for PyPI"

2. **Publish to TestPyPI**: Uploads the package to TestPyPI first (recommended for testing)
   - Press `Ctrl+Shift+P`, select "Tasks: Run Task", then "Publish to TestPyPI"

3. **Publish to PyPI**: Uploads the package to the main PyPI repository
   - Press `Ctrl+Shift+P`, select "Tasks: Run Task", then "Publish to PyPI"

### Manual Steps (If Needed)

If you prefer to run commands manually:

1. **Build the package**:
   ```
   python -m build
   ```

2. **Check the distribution**:
   ```
   twine check dist/*
   ```

3. **Upload to TestPyPI** (recommended for testing first):
   ```
   twine upload --repository testpypi dist/*
   ```

4. **Upload to PyPI**:
   ```
   twine upload dist/*
   ```

## Installation After Publishing

Once published, users can install your package using pip:

```
# From TestPyPI
pip install --index-url https://test.pypi.org/simple/ blogger-cli

# From PyPI
pip install blogger-cli
```

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Publishing Documentation](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine Documentation](https://twine.readthedocs.io/)
