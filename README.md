# Vue Blogger SPA - Experimental Blog UI Enhancement

An experimental Single Page Application (SPA) built with Vue.js to replace and modernize a Blogger page interface. This project aims to provide a more contemporary and user-friendly blog experience while maintaining compatibility with the existing Blogger platform.

## 🚀 Project Overview

This is an experimental project designed to enhance my wife's blog UI by replacing the default Blogger interface with a modern Vue.js application. The goal is to create a more engaging and responsive reading experience while preserving all existing blog functionality.

## 📋 Architecture

- **Frontend**: Vue.js SPA with static files on GitHub
- **CDN**: jsDelivr for serving JavaScript files
- **Backend**: Blogger platform (unchanged)
- **Entry Point**: `index.js` file hosted directly on Blogger

## 🛠️ Tech Stack

- **Vue.js** - Progressive JavaScript framework
- **GitHub** - Code repository and version control
- **jsDelivr** - CDN for serving JavaScript files
- **Blogger** - Content management and hosting platform

## 🔧 Configuration

### Blogger API Key
This project requires a Blogger API key to fetch blog content. The API key is stored in `.env` file and excluded from the repository via `.gitignore`.

To set up:
1. Create a `.env` file in the root directory
2. Add your Blogger API key: `BLOGGER_API_KEY=your_api_key_here`
3. The `.env` file is already included in `.gitignore` and will not be committed

### CSS Template
The main CSS file is excluded from the repository. A template is provided in the `css/` directory for those who want to launch this app. Copy and customize the template according to your blog's design requirements.

## ⚠️ Experimental Status

This project is currently in **experimental phase**. Features and implementation may change significantly as development progresses.

## 🎯 Goals

- [ ] Improve blog loading speed and performance
- [ ] Enhance mobile responsiveness
- [ ] Modernize the overall user interface
- [ ] Maintain all existing Blogger functionality
- [ ] Add new interactive features for better user engagement

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to the Vue.js community for excellent documentation and tools
- Inspired by modern web design principles and user experience best practices

---

**Note**: This is an experimental project aimed at enhancing a personal blog. Use at your own discretion and always test thoroughly before deploying to production.
