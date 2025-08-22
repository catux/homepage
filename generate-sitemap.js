#!/usr/bin/env node

const fs = require('fs')
const path = require('path')
const { promisify } = require('util')
const { globSync } = require('glob')
const readFileAsync = promisify(fs.readFile)
const writeFileAsync = promisify(fs.writeFile)

/**
 * Generate sitemap.xml for the website
 * This script scans the public directory for HTML files and creates a sitemap.xml file
 */
async function generateSitemap () {
  try {
    // Read the base URL from context file
    const contextData = await readFileAsync('app/src/templates/context/_all.json', 'utf-8')
    const baseUrl = JSON.parse(contextData).homepage

    // Get all HTML files in the public directory
    const publicDir = 'app/public'
    const htmlFiles = globSync(`${publicDir}/**/*.html`)

    // Start building the sitemap XML
    let sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    // Add each HTML file to the sitemap
    htmlFiles.forEach(file => {
      // Get relative path from public directory
      const relativePath = path.relative(publicDir, file)
      // Create full URL
      const url = new URL(relativePath, baseUrl).href

      // Add URL to sitemap
      sitemap += '  <url>\n'
      sitemap += `    <loc>${url}</loc>\n`
      sitemap += `    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>\n`
      sitemap += '    <changefreq>monthly</changefreq>\n'
      sitemap += '    <priority>0.8</priority>\n'
      sitemap += '  </url>\n'
    })

    // Close the sitemap XML
    sitemap += '</urlset>'

    // Write the sitemap to file
    await writeFileAsync('app/public/sitemap.xml', sitemap, 'utf-8')

    console.log('Sitemap generated successfully!')
  } catch (error) {
    console.error('Error generating sitemap:', error)
    process.exit(1)
  }
}

// Run the function
generateSitemap()
