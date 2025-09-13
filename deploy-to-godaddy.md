# Deploy Square Transport Website to GoDaddy

## Prerequisites
- GoDaddy web hosting account
- FTP credentials from GoDaddy cPanel

## Step 1: Get FTP Credentials
1. Login to GoDaddy cPanel
2. Go to "FTP Accounts" 
3. Note down:
   - FTP Server: Usually `yourdomain.com` or `ftp.yourdomain.com`
   - Username: Usually your main cPanel username
   - Password: Your cPanel password
   - Port: Usually 21 (FTP) or 22 (SFTP)

## Step 2: Upload Files
Using an FTP client (like FileZilla):

1. Connect to your FTP server
2. Navigate to `/public_html/` directory
3. Upload ALL contents from `c:\square\dist\` folder
4. Ensure files are in root of public_html, not a subfolder

## File Structure on Server
```
public_html/
├── index.html
├── about.html  
├── overview.html
└── assets/
    ├── *.css files
    ├── *.js files
    ├── *.png files
    └── Product-d6adbd84.mp4
```

## Step 3: Test Your Website
Visit your domain: `https://yourdomain.com`

## Troubleshooting
- If you see a "Coming Soon" page, files may be in wrong location
- Ensure index.html is in the root of public_html
- Check file permissions (should be 644 for files, 755 for folders)
- Clear browser cache if changes don't appear

## Future Updates
To update your website:
1. Make changes to your source files
2. Run `npm run build` 
3. Upload new contents of `dist/` folder to `public_html/`
