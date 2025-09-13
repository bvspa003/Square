# Square Transport Website: GitHub to GoDaddy Deployment Guide

## Overview
This guide shows how to host your Square Transport website on GitHub and use your GoDaddy domain to point to it. This approach gives you:
- ✅ Free hosting on GitHub Pages
- ✅ Automatic deployments when you update code
- ✅ Professional development workflow
- ✅ Version control and backup
- ✅ Use your custom GoDaddy domain
- ✅ HTTPS certificate included

## Prerequisites
- GitHub account (free)
- Your GoDaddy domain
- Access to GoDaddy DNS settings

---

## Step 1: Prepare Your Project for GitHub

### 1.1 Initialize Git Repository
```bash
# In your c:\square folder
git init
git add .
git commit -m "Initial commit: Square Transport website"
```

### 1.2 Create .gitignore File
Create `.gitignore` to exclude unnecessary files:
```
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/
*.zip

# Environment files
.env
.env.local
.env.production

# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd

# OS files
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp
*.swo
```

---

## Step 2: Set Up GitHub Repository

### 2.1 Create Repository on GitHub
1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name it: `square-transport-website`
4. Make it **Public** (required for free GitHub Pages)
5. Don't initialize with README (you already have files)
6. Click "Create repository"

### 2.2 Connect Local Repository to GitHub
```bash
# Replace 'yourusername' with your actual GitHub username
git remote add origin https://github.com/yourusername/square-transport-website.git
git branch -M main
git push -u origin main
```

---

## Step 3: Set Up Automatic Deployment

### 3.1 Create GitHub Actions Workflow
Create folder structure: `.github/workflows/`
Create file: `.github/workflows/deploy.yml`

```yaml
name: Deploy Square Transport Website

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Build website
      run: npm run build
      
    - name: Setup Pages
      uses: actions/configure-pages@v4
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: ./dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    
    steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
```

### 3.2 Update Vite Configuration
Ensure your `vite.config.js` has the correct base path:

```javascript
export default defineConfig({
  root: 'src',
  base: '/', // This ensures assets load correctly
  // ... rest of your config
});
```

---

## Step 4: Enable GitHub Pages

### 4.1 Configure Pages in Repository Settings
1. Go to your GitHub repository
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**, select "GitHub Actions"
5. Save the configuration

### 4.2 Trigger First Deployment
```bash
# Make a small change and push to trigger deployment
echo "# Square Transport Website" > README.md
git add README.md
git commit -m "Add README for GitHub Pages"
git push
```

---

## Step 5: Configure Your GoDaddy Domain

### 5.1 Add Custom Domain in GitHub
1. In GitHub Pages settings, add your domain: `yourdomain.com`
2. This creates a `CNAME` file in your repository
3. Enable "Enforce HTTPS" option

### 5.2 Update GoDaddy DNS Settings
In your GoDaddy Domain Manager:

**For Root Domain (yourdomain.com):**
- Type: `A` | Name: `@` | Value: `185.199.108.153`
- Type: `A` | Name: `@` | Value: `185.199.109.153`
- Type: `A` | Name: `@` | Value: `185.199.110.153`
- Type: `A` | Name: `@` | Value: `185.199.111.153`

**For WWW Subdomain:**
- Type: `CNAME` | Name: `www` | Value: `yourusername.github.io`

**Important:** Replace `yourusername` with your actual GitHub username!

---

## Step 6: Verify Deployment

### 6.1 Check GitHub Actions
1. Go to your repository
2. Click **Actions** tab
3. You should see your workflow running/completed
4. Green checkmark = successful deployment

### 6.2 Test Your Website
1. Visit: `https://yourusername.github.io/square-transport-website`
2. After DNS propagation (up to 24 hours): `https://yourdomain.com`

---

## Development Workflow

### Making Updates
1. Edit your files in `src/` folder
2. Test locally: `npm run dev`
3. Commit and push changes:
   ```bash
   git add .
   git commit -m "Update website content"
   git push
   ```
4. GitHub automatically builds and deploys!

### Local Development
```bash
# Start development server
npm run dev

# Build for production (test before pushing)
npm run build

# Preview production build
npm run preview
```

---

## Troubleshooting

### Common Issues:
1. **404 Error**: Check that `index.html` is in the `dist` folder after build
2. **CSS/JS Not Loading**: Verify `base: '/'` in `vite.config.js`
3. **DNS Not Working**: Wait up to 24 hours for propagation
4. **Build Failing**: Check the Actions tab for error details

### Useful Commands:
```bash
# Check build output
ls dist/

# Test DNS propagation
nslookup yourdomain.com

# Force rebuild
git commit --allow-empty -m "Trigger rebuild"
git push
```

---

## Benefits of This Setup

✅ **Free Hosting**: GitHub Pages is completely free
✅ **Automatic Deployments**: Every git push updates your website
✅ **Professional Workflow**: Industry-standard development practices
✅ **Backup & History**: Your code is safely stored and versioned
✅ **Custom Domain**: Use your GoDaddy domain with HTTPS
✅ **Fast Performance**: GitHub's CDN delivers your site globally
✅ **Collaboration Ready**: Easy to work with team members

Your Square Transport website will be live on your custom domain with professional deployment automation!
