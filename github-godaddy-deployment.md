# Deploy Square Transport Website: GitHub → GoDaddy Domain

## Option 1: GitHub Pages with Custom Domain (Recommended)

### Step 1: Push Your Code to GitHub
```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit: Square Transport website"

# Create repository on GitHub and push
git remote add origin https://github.com/yourusername/square-transport-website.git
git branch -M main
git push -u origin main
```

### Step 2: Set Up GitHub Pages
1. Go to your GitHub repository
2. Click **Settings** tab
3. Scroll to **Pages** section
4. Under **Source**, select "GitHub Actions"
5. Create `.github/workflows/deploy.yml` (see below)

### Step 3: Configure Custom Domain
1. In GitHub Pages settings, add your domain: `yourdomain.com`
2. Enable "Enforce HTTPS"
3. GitHub will create a CNAME file

### Step 4: Update GoDaddy DNS
In your GoDaddy DNS settings:
- **A Record**: `@` → `185.199.108.153`
- **A Record**: `@` → `185.199.109.153` 
- **A Record**: `@` → `185.199.110.153`
- **A Record**: `@` → `185.199.111.153`
- **CNAME**: `www` → `yourusername.github.io`

---

## Option 2: Netlify with GitHub (Alternative)

### Benefits:
- Automatic deployments on git push
- Built-in CDN and HTTPS
- Environment variables support
- Branch previews

### Setup:
1. Connect Netlify to your GitHub repo
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Point your GoDaddy domain to Netlify

---

## Option 3: Vercel with GitHub (Alternative)

### Benefits:
- Serverless functions support
- Automatic deployments
- Great performance
- Easy custom domains

---

## GitHub Actions Workflow
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
      
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Build
      run: npm run build
      
    - name: Deploy to GitHub Pages
      uses: actions/deploy-pages@v2
      with:
        folder: dist
```

## Benefits of GitHub + Custom Domain:
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ Version control
- ✅ Collaboration friendly
- ✅ HTTPS included
- ✅ CDN performance
- ✅ Keep your GoDaddy domain
- ✅ Professional workflow
