const nunjucks = require('nunjucks')
const fs = require('fs')
const path = require('path')
const { globSync } = require('glob')

// Configure Nunjucks
const templatesDir = 'app/src/templates'
const outputDir = 'app/public'
nunjucks.configure(templatesDir, {
  autoescape: true,
  noCache: false
})

// Load context files
let context = {}
try {
  const contextFiles = globSync('app/src/templates/context/**/*.json')
  contextFiles.forEach(file => {
    const contextData = JSON.parse(fs.readFileSync(file, 'utf8'))
    context = { ...context, ...contextData }
  })
} catch (error) {
  console.error('Error loading context files:', error)
}

// Define templates to render
const templates = [
  'index.html',
  'post_list.html',
  'contactar.html',
  'traduccio.html',
  ...globSync('app/src/templates/posts/*.html').map(file => path.relative(templatesDir, file))
]

// Ensure output directory exists
function ensureDirectoryExists (dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true })
  }
}

// Render templates
templates.forEach(template => {
  try {
    const outputPath = path.join(outputDir, template)
    const outputDirectory = path.dirname(outputPath)

    // Ensure the output directory exists
    ensureDirectoryExists(outputDirectory)

    // Render the template
    const renderedContent = nunjucks.render(template, context)

    // Write the rendered content to file
    fs.writeFileSync(outputPath, renderedContent)
    console.log(`Rendered: ${template} -> ${outputPath}`)
  } catch (error) {
    console.error(`Error rendering ${template}:`, error)
  }
})

console.log('Template rendering complete!')
