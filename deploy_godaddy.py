#!/usr/bin/env python3
"""
Square Transport Website - GoDaddy One-Step Deployment
Similar to run_app.py but deploys to GoDaddy hosting
"""

import os
import sys
import platform
import subprocess
import shutil
import zipfile
import ftplib
import webbrowser
from pathlib import Path
import time

# Try to import dotenv, but don't require it
try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False
    def load_dotenv():
        pass

class SquareGoDaddyDeployer:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / 'dist'
        self.os_info = self.detect_system()
        
        # Load environment variables for FTP credentials
        load_dotenv()
        
    def detect_system(self):
        """Detect operating system and return detailed information"""
        system_info = {
            'name': platform.system(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'python_version': sys.version,
            'platform': platform.platform()
        }
        
        if system_info['name'] == 'Windows':
            system_info.update({
                'shell': 'cmd'
            })
        elif system_info['name'] == 'Darwin':  # macOS
            system_info.update({
                'shell': 'zsh'
            })
        elif system_info['name'] == 'Linux':
            system_info.update({
                'shell': 'bash'
            })
        
        return system_info

    def check_npm_availability(self):
        """Check if npm is available and return status"""
        try:
            print("🔍 Checking for npm...")
            result = subprocess.run(['npm', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10,
                                  shell=True)
            if result.returncode == 0:
                npm_version = result.stdout.strip()
                print(f"✅ npm found (version {npm_version})")
                return True
            else:
                print("❌ npm not found")
                return False
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            print("❌ npm not available")
            return False

    def build_website(self):
        """Build the website using Vite"""
        print("\n🔨 Building Square Transport website...")
        try:
            result = subprocess.run(['npm', 'run', 'build'], 
                                  cwd=self.root_dir, 
                                  check=True, 
                                  shell=True)
            print("✅ Website built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            return False

    def create_deployment_package(self):
        """Create deployment package for manual upload"""
        print("📦 Creating deployment package...")
        
        zip_path = self.root_dir / 'square-transport-godaddy-deploy.zip'
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.dist_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.dist_dir)
                    zipf.write(file_path, arcname)
                    print(f"  📄 Added: {arcname}")
        
        print(f"✅ Deployment package created: {zip_path}")
        return zip_path

    def setup_ftp_config(self):
        """Setup FTP configuration interactively or from environment"""
        env_file = self.root_dir / '.env'
        
        # Check if FTP credentials exist
        ftp_host = os.getenv('GODADDY_FTP_HOST')
        ftp_username = os.getenv('GODADDY_FTP_USERNAME')
        ftp_password = os.getenv('GODADDY_FTP_PASSWORD')
        
        if not all([ftp_host, ftp_username, ftp_password]):
            print("\n🔧 FTP Configuration Setup")
            print("=" * 40)
            print("To enable automatic FTP deployment, add these to your .env file:")
            print("")
            print("GODADDY_FTP_HOST=yourdomain.com")
            print("GODADDY_FTP_USERNAME=your_username")
            print("GODADDY_FTP_PASSWORD=your_password")
            print("GODADDY_DOMAIN=https://yourdomain.com")
            print("")
            print("You can find these in your GoDaddy cPanel under 'FTP Accounts'")
            return False
        
        return True

    def deploy_via_ftp(self):
        """Deploy website via FTP to GoDaddy"""
        if not self.setup_ftp_config():
            return False
            
        print("\n🚀 Deploying to GoDaddy via FTP...")
        
        try:
            ftp_host = os.getenv('GODADDY_FTP_HOST')
            ftp_username = os.getenv('GODADDY_FTP_USERNAME') 
            ftp_password = os.getenv('GODADDY_FTP_PASSWORD')
            
            # Connect to FTP
            ftp = ftplib.FTP(ftp_host)
            ftp.login(ftp_username, ftp_password)
            
            # Change to public_html directory
            try:
                ftp.cwd('/public_html')
            except:
                ftp.cwd('/htdocs')  # Some hosts use htdocs
            
            print("📡 Connected to GoDaddy FTP server")
            
            # Upload files
            self.upload_directory_ftp(ftp, self.dist_dir, '/')
            
            ftp.quit()
            print("✅ FTP deployment completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ FTP deployment failed: {e}")
            return False

    def upload_directory_ftp(self, ftp, local_dir, remote_dir):
        """Recursively upload directory via FTP"""
        for item in local_dir.iterdir():
            if item.is_file():
                print(f"📤 Uploading: {item.name}")
                with open(item, 'rb') as f:
                    ftp.storbinary(f'STOR {item.name}', f)
            elif item.is_dir():
                # Create remote directory
                try:
                    ftp.mkd(item.name)
                except:
                    pass  # Directory might already exist
                ftp.cwd(item.name)
                self.upload_directory_ftp(ftp, item, remote_dir + item.name + '/')
                ftp.cwd('..')

    def open_website(self):
        """Open the deployed website in browser"""
        domain = os.getenv('GODADDY_DOMAIN')
        if domain:
            print(f"\n🌐 Opening website: {domain}")
            try:
                webbrowser.open(domain)
            except:
                print(f"Please visit: {domain}")
        else:
            print("\n🌐 Add GODADDY_DOMAIN=https://yourdomain.com to .env to auto-open website")

    def deploy_to_godaddy(self):
        """Main deployment method - tries FTP first, falls back to manual"""
        print("🚀 Square Transport GoDaddy Deployment Started")
        print(f"📊 Detected OS: {self.os_info['name']} {self.os_info['platform']}")
        print("=" * 60)
        
        # Step 1: Check npm
        if not self.check_npm_availability():
            print("\n❌ npm/Node.js not found!")
            print("🔧 Please install Node.js from: https://nodejs.org/")
            sys.exit(1)
        
        # Step 2: Build website
        if not self.build_website():
            sys.exit(1)
        
        # Step 3: Try FTP deployment first
        print("\n🎯 Attempting automatic FTP deployment...")
        ftp_success = self.deploy_via_ftp()
        
        if ftp_success:
            print("\n" + "=" * 60)
            print("✅ Automatic deployment completed successfully!")
            print("🌐 Your Square Transport website is now live!")
            self.open_website()
        else:
            # Step 4: Fallback to manual deployment
            print("\n📦 Creating manual deployment package...")
            zip_path = self.create_deployment_package()
            
            print("\n" + "=" * 60)
            print("📋 Manual Deployment Instructions:")
            print("=" * 60)
            print("1. Login to your GoDaddy cPanel")
            print("2. Open File Manager")
            print("3. Navigate to public_html folder")
            print("4. Delete any existing files")
            print(f"5. Upload and extract: {zip_path.name}")
            print("6. Ensure files are in root of public_html")
            print("7. Visit your domain!")
        
        self.show_file_structure()
        
        return True

    def show_file_structure(self):
        """Show what files will be deployed"""
        if not self.dist_dir.exists():
            print("❌ No build found. Run 'npm run build' first.")
            return
        
        print("\n📁 Files deployed to GoDaddy:")
        print("-" * 40)
        for file_path in sorted(self.dist_dir.rglob('*')):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.dist_dir)
                file_size = file_path.stat().st_size
                if file_size > 1024*1024:  # > 1MB
                    size_str = f"{file_size / (1024*1024):.1f}MB"
                elif file_size > 1024:  # > 1KB  
                    size_str = f"{file_size / 1024:.1f}KB"
                else:
                    size_str = f"{file_size}B"
                print(f"  {relative_path} ({size_str})")

    def run(self):
        """Main entry point - similar to run_app.py"""
        try:
            return self.deploy_to_godaddy()
        except KeyboardInterrupt:
            print("\n👋 Deployment interrupted by user.")
        except Exception as e:
            print(f"❌ Deployment failed: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    deployer = SquareGoDaddyDeployer()
    deployer.run()
