# Vue Blogger SPA

A Vue.js Single Page Application designed to be embedded in Blogger sites. This project provides a modern, interactive blog interface that can be integrated into Blogger's platform.

> **⚠️ Warning:** This project is in an early development stage. Some features may be incomplete or contain bugs. Use in production environments at your own risk.

## Features

- TypeScript for type safety
- Vue Router for SPA navigation
- Pinia for state management
- Blog post listing with tag filtering
- Individual post view
- Responsive design
- Single-file embedding for Blogger

## Project Setup

```sh
# Install dependencies
npm install

# Create .env file with your Blogger API credentials
# Create a file named .env.local with the following content:
# VITE_BLOGGER_API_KEY=your_api_key_here
# VITE_BLOGGER_BLOG_ID=your_blog_id_here

# Start development server
npm run dev

# Build for production
npm run build

# Build single-file version for Blogger
npm run build:blogger

# Preview the production build
npm run preview
```

## Embedding in Blogger

This Vue.js application can be embedded into a Blogger post in two different ways:

### Option 1: Single HTML File (May not work with all Blogger templates)

1. Run the Blogger-specific build:
   ```sh
   npm run build:blogger
   ```

2. This creates a single HTML file (`dist-blogger/index.html`) containing the entire application with all assets inlined

3. Open the generated file and copy all of its content

4. In Blogger, create a new post, switch to HTML view, and paste the copied content

### Option 2: External JavaScript File (Recommended)

If the single HTML file approach doesn't work due to Blogger's restrictions, use this approach:

1. Run the JavaScript build command:
   ```sh
   npm run build:blogger-js
   ```

2. This creates an `index.js` file in the `dist-blogger` directory

3. Host this JavaScript file somewhere accessible (GitHub Pages, Netlify, Vercel, etc.)

4. In your Blogger post, add the following HTML code (in HTML view):
   ```html
   <div id="app"></div>
   <script>
     (function() {
       // Load the Vue application script
       const script = document.createElement('script');
       script.src = 'YOUR_HOSTING_URL/index.js'; // Replace with your actual hosting URL
       script.async = true;
       document.body.appendChild(script);
     })();
   </script>
   ```

5. Replace `YOUR_HOSTING_URL` with the actual URL where you've hosted the index.js file

This approach separates the JavaScript code from your Blogger post, making it more likely to work with Blogger's content restrictions.

## Project Structure

- `src/components/` - Reusable Vue components
- `src/views/` - Page components
- `src/router/` - Vue Router configuration
- `src/stores/` - Pinia stores for state management
- `src/data/` - Sample data for the blog

## Customization

To customize the blog content:

1. Edit the sample posts in `src/data/posts.ts`
2. Modify component styles as needed
3. Add additional routes in `src/router/index.ts`

> **Note:** The Blogger API integration may require additional configuration or may return data in unexpected formats. The application includes error handling and fallbacks to sample data when API calls fail.

## Type Support for `.vue` Imports in TypeScript

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Development Commands

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with ESLint

```sh
npm run lint
```

## Known Issues

- **Blogger API Integration**: The Blogger API may return data in various formats depending on your blog's configuration. The application attempts to handle these variations, but you may encounter unexpected behaviors.
- **Page Navigation**: Some Blogger page URLs may not be properly detected or rendered within the SPA.
- **Content Rendering**: Complex HTML content from Blogger posts/pages may not render exactly as it appears on the original blog.
- **API Rate Limiting**: Be aware of Google API usage limits when fetching data frequently.

If you encounter any issues, please check the browser console for error messages and consider using the fallback sample data until the integration is more stable.
