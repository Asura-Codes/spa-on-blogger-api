import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig(() => {
  // Load .env variables using Vite's loadEnv
  const env = loadEnv('', process.cwd(), '')
  const jsDelivrBase = env.VITE_JSDELIVR_BASE_URL || '{{JSDELIVR_BASE_URL}}'

  return {
    plugins: [
      vue(),
      {
        name: 'update-jsdelivr-urls',
        closeBundle: () => {
          try {
            const distPath = path.resolve(__dirname, 'dist-jsdelivr')
            console.log('Looking for files in:', distPath)

            const files = fs.readdirSync(distPath)
            console.log('Files in directory:', files)

            // Find JS and CSS files that match index pattern
            const jsFile = files.find(file => file.match(/^index\..*\.js$/))
            const cssFile = files.find(file => file.match(/^index\..*\.css$/))

            console.log('Found JS file:', jsFile)
            console.log('Found CSS file:', cssFile)

            if (jsFile && cssFile) {
              // Update the index.html file to use jsDelivr URLs
              const indexHtmlPath = path.join(distPath, 'index.html')
              let indexHtml = fs.readFileSync(indexHtmlPath, 'utf8')

              // Replace relative JS path with jsDelivr path
              indexHtml = indexHtml.replace(
                `<script type="module" crossorigin src="./index.${jsFile.split('.')[1]}.js"></script>`,
                `<script type="module" crossorigin="anonymous" src="${jsDelivrBase}/${jsFile}"></script>`
              )

              // Replace relative CSS path with jsDelivr path
              indexHtml = indexHtml.replace(
                `<link rel="stylesheet" crossorigin href="./index.${cssFile.split('.')[1]}.css">`,
                `<link rel="stylesheet" crossorigin="anonymous" href="${jsDelivrBase}/${cssFile}"/>`
              )

              // Also update title to be more descriptive
              indexHtml = indexHtml.replace(
                '<title>Vite App</title>',
                '<title><data:view.title.escaped/></title>\n<b:skin><![CDATA[ /* Your theme\'s CSS goes here */ ]]></b:skin>'
              )

              // Make sure the Blogger variables capture script is preserved
              // This regex looks for the script tag that captures Blogger variables
              if (!indexHtml.includes('window.bloggerData')) {
                const headEndTag = '</head>';
                const bloggerVarScript = `<script>
                  // Initialize global object to store Blogger variables
                  window.bloggerData = {
                    blog: { title: '', url: '', homepageUrl: '', pageName: '', pageType: '', locale: '', isMobile: false },
                    post: { id: '', title: '', url: '', author: '', timestamp: '', content: '' },
                    page: { id: '', title: '', url: '' }
                  };

                  // Function to capture Blogger variables when running in Blogger environment
                  (function captureBloggerVariables() {
                    if (typeof data !== 'undefined') {
                      try {
                        if (data.blog) {
                          window.bloggerData.blog = Object.assign(window.bloggerData.blog, data.blog);
                        }
                        if (data.posts && data.posts.length > 0) {
                          window.bloggerData.post = Object.assign(window.bloggerData.post, data.posts[0]);
                        }
                        if (data.pages && data.pages.length > 0) {
                          window.bloggerData.page = Object.assign(window.bloggerData.page, data.pages[0]);
                        }
                        console.log('Blogger variables captured');
                      } catch (e) {
                        console.error('Error capturing Blogger variables:', e);
                      }
                    }
                  })();
                </script>`;

                indexHtml = indexHtml.replace(headEndTag, bloggerVarScript + headEndTag);
              }

              // Insert Blogger sidebar section into <body>
              indexHtml = indexHtml.replace(
                '<div id="app"></div>',
                `<div id="app"></div>\n<b:section class='sidebar' id='sidebar' showaddelement='yes'/>`
              )

              // Write updated HTML back to file
              fs.writeFileSync(indexHtmlPath, indexHtml)
              console.log(`Updated index.html with jsDelivr URL placeholders`)
              console.log(`JS: ${jsDelivrBase}/${jsFile}`)
              console.log(`CSS: ${jsDelivrBase}/${cssFile}`)

              // Make a copy as blogger-template.html for convenience
              fs.copyFileSync(indexHtmlPath, path.join(distPath, 'blogger-template.html'))
              console.log('Created a copy as blogger-template.html')

              console.log('\n========================================')
              console.log('DEPLOYMENT INSTRUCTIONS:')
              console.log('========================================')
              console.log('1. Push your code to GitHub')
              console.log('2. Replace the placeholder {{JSDELIVR_BASE_URL}} in blogger-template.html with your jsDelivr URL:')
              console.log('   https://cdn.jsdelivr.net/gh/USERNAME/REPO@VERSION/vue-blogger-spa/dist-jsdelivr')
              console.log('3. Copy the contents of blogger-template.html to your Blogger template')
              console.log('========================================\n')
            } else {
              console.error('Missing JS or CSS files in the dist-jsdelivr directory')
            }
          } catch (error) {
            console.error('Error updating jsDelivr URLs:', error)
          }
        }
      }
    ],
    base: './', // Use relative base path for local testing
    build: {
      outDir: 'dist-jsdelivr',
      assetsDir: '', // Keep all assets at the root
      rollupOptions: {
        output: {
          entryFileNames: 'index.[hash].js',
          chunkFileNames: '[name].[hash].js',
          assetFileNames: '[name].[hash].[ext]'
        }
      }
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    }
  }
})
