#!/usr/bin/env node

const fs = require('fs')
const path = require('path')
const { promisify } = require('util')
const readFileAsync = promisify(fs.readFile)
const writeFileAsync = promisify(fs.writeFile)
const readdirAsync = promisify(fs.readdir)
const statAsync = promisify(fs.stat)

// Template for the post list
const template = `
{% extends 'post_list_template.html' %}

{% block links %}
 {0}
{% endblock %}
`

// Function to walk through a directory recursively
async function walkDir (dir) {
  const files = await readdirAsync(dir)
  const fileList = []

  for (const file of files) {
    const filePath = path.join(dir, file)
    const stats = await statAsync(filePath)

    if (stats.isDirectory()) {
      const subFiles = await walkDir(filePath)
      fileList.push(...subFiles)
    } else {
      fileList.push(filePath)
    }
  }

  return fileList
}

// Function to extract content using regex
function extractContent (content, pattern) {
  const matches = content.match(pattern)
  if (matches && matches[1]) {
    return matches[1].trim()
  }
  return ''
}

async function generatePostList () {
  try {
    // Read the host from context file
    const contextData = await readFileAsync('app/src/templates/context/_all.json', 'utf-8')
    const HOST = JSON.parse(contextData).homepage

    // Array to store links
    const LINKS = []

    // Get all post files
    const postsDir = 'app/src/templates/posts/'
    const files = await walkDir(postsDir)

    // Process each file
    for (const filename of files) {
      const content = await readFileAsync(filename, 'utf-8')

      // Extract information using regex patterns similar to the Python script
      const title = extractContent(content, /title %\}([^}]+)\{/)
      const postDate = extractContent(content, /post_date %\}([^}]+)\{/)
      const author = extractContent(content, /author %\}([^}]+)\{/)

      if (title && postDate && author) {
        const relPath = path.relative('app/src/templates/', filename)

        LINKS.push([
          postDate,
          `<li class="list-group-item"><a class="blog-post" href="${HOST}${relPath}">${title} <div class="float-end hidden-xs"><span class="badge blog-date">${author}</span>&nbsp;<span class="badge blog-date">${postDate}</span></div></a></li>\n`
        ])
      }
    }

    // Sort links by date in descending order
    const orderedLinks = LINKS.sort((a, b) => {
      if (a[0] > b[0]) return -1
      if (a[0] < b[0]) return 1
      return 0
    })

    // Generate content
    const content = template.replace('{0}', orderedLinks.map(link => link[1]).join(''))

    // Write to file
    await writeFileAsync('app/src/templates/post_list.html', content, 'utf-8')

    console.log('Post list generated successfully!')
  } catch (error) {
    console.error('Error generating post list:', error)
    process.exit(1)
  }
}

// Run the function
generatePostList()
