import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory name of the current module
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Function to update the template HTML with the correct JS file name
function updateTemplateWithJsFileName() {
  const distPath = path.join(__dirname, '..', 'dist-blogger');
  const templatePath = path.join(__dirname, '..', 'public', 'index-template.html');
  const outputTemplatePath = path.join(distPath, 'index-template.html');

  console.log('Looking for JS files in:', distPath);

  try {
    // Read the directory to find the JS file with hash
    const files = fs.readdirSync(distPath);
    const jsFile = files.find(file => file.startsWith('index.') && file.endsWith('.js'));

    if (!jsFile) {
      console.error('No JS file found in the dist-blogger directory');
      return;
    }

    console.log(`Found JS file: ${jsFile}`);

    // Read the template HTML
    let templateHtml = fs.readFileSync(templatePath, 'utf8');

    // Replace the placeholder with the actual file name
    templateHtml = templateHtml.replace(
      /script\.src = '(.*)index\.js'/,
      `script.src = '$1${jsFile}'`
    );

    // Write the updated template to the dist directory
    fs.writeFileSync(outputTemplatePath, templateHtml);

    // Also create a blogger-snippet.html file
    const bloggerSnippet = `<!-- Vue Blogger SPA -->
<div id="app"></div>
<script>
  (function() {
    // Load the Vue application script
    const script = document.createElement('script');
    script.src = 'YOUR_HOSTING_URL/${jsFile}'; // Replace YOUR_HOSTING_URL with your actual hosting URL
    script.async = true;
    document.body.appendChild(script);
  })();
</script>`;

    fs.writeFileSync(path.join(distPath, 'blogger-snippet.html'), bloggerSnippet);

    console.log('Successfully updated template HTML with correct JS file name');
    console.log('Files created:');
    console.log(`- ${outputTemplatePath}`);
    console.log(`- ${path.join(distPath, 'blogger-snippet.html')}`);

  } catch (error) {
    console.error('Error updating template HTML:', error);
  }
}

// Run the update function
updateTemplateWithJsFileName();
