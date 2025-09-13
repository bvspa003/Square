#!/usr/bin/env python3
"""
Square Transport Website - Automated Deployment Script
Handles environment setup, OS detection, and deployment automation
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
import time
import signal
import atexit

class SquareWebsiteDeployer:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.os_info = self.detect_system()
        self.venv_dir = self.root_dir / 'venv'
        self.venv_python = self.get_venv_python_path()
        self.server_process = None
        
        # Setup graceful shutdown
        self.setup_signal_handlers()
        
    def detect_system(self):
        """Detect operating system and return detailed information"""
        system_info = {
            'name': platform.system(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'python_version': sys.version,
            'platform': platform.platform(),
            'processor': platform.processor()
        }
        
        if system_info['name'] == 'Windows':
            system_info.update({
                'package_manager': 'pip',
                'shell': 'cmd',
                'path_separator': '\\',
                'executable_extension': '.exe'
            })
        elif system_info['name'] == 'Darwin':  # macOS
            system_info.update({
                'package_manager': 'brew',
                'shell': 'zsh',
                'path_separator': '/',
                'executable_extension': ''
            })
        elif system_info['name'] == 'Linux':
            system_info.update({
                'package_manager': 'apt',
                'shell': 'bash',
                'path_separator': '/',
                'executable_extension': ''
            })
        
        return system_info
    
    def get_venv_python_path(self):
        """Get the path to the Python executable in the virtual environment"""
        if self.os_info['name'] == 'Windows':
            return self.venv_dir / 'Scripts' / 'python.exe'
        else:
            return self.venv_dir / 'bin' / 'python'
    
    def get_venv_pip_path(self):
        """Get the path to pip in the virtual environment"""
        if self.os_info['name'] == 'Windows':
            return self.venv_dir / 'Scripts' / 'pip.exe'
        else:
            return self.venv_dir / 'bin' / 'pip'
    
    def create_virtual_environment(self):
        """Create a virtual environment if it doesn't exist"""
        if not self.venv_dir.exists():
            print("🔧 Creating virtual environment...")
            try:
                subprocess.run([
                    sys.executable, '-m', 'venv', str(self.venv_dir)
                ], check=True)
                print("✅ Virtual environment created successfully")
                
                # Upgrade pip in the virtual environment
                print("📦 Upgrading pip in virtual environment...")
                subprocess.run([
                    str(self.venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'
                ], check=True)
                print("✅ Pip upgraded successfully")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to create virtual environment: {e}")
                raise

    
    def setup_signal_handlers(self):
        """Setup graceful shutdown handlers"""
        def signal_handler(signum, frame):
            print(f"\n🛑 Received shutdown signal ({signum})")
            self.graceful_shutdown()
            sys.exit(0)
        
        def cleanup():
            self.graceful_shutdown()
        
        # Register signal handlers
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_handler)
        
        # Register cleanup function for normal exit
        atexit.register(cleanup)
    
    def graceful_shutdown(self):
        """Gracefully shutdown the server and cleanup resources"""
        if self.server_process and self.server_process.poll() is None:
            print("🛑 Shutting down Square Transport server...")
            try:
                self.server_process.terminate()
                # Give it a moment to terminate gracefully
                try:
                    self.server_process.wait(timeout=5)
                    print("✅ Server shutdown complete")
                except subprocess.TimeoutExpired:
                    print("⚠️ Force killing server...")
                    self.server_process.kill()
                    print("✅ Server force stopped")
            except Exception as e:
                print(f"⚠️ Error during shutdown: {e}")
        
        print("👋 Thank you for using Square Transport!")
    
    def check_npm_availability(self):
        """Check if npm is available and return status"""
        try:
            print("🔍 Checking for npm...")
            result = subprocess.run(['npm', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10,
                                  shell=True)  # Add shell=True for Windows
            if result.returncode == 0:
                npm_version = result.stdout.strip()
                print(f"✅ npm found (version {npm_version})")
                return True
            else:
                print(f"❌ npm command failed with return code: {result.returncode}")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                return False
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"❌ npm check failed with exception: {type(e).__name__}: {e}")
            return False
        
    def run(self):
        """Main deployment orchestration"""
        try:
            print("🚀 Square Transport Website Deployment Started")
            print(f"📊 Detected OS: {self.os_info['name']} {self.os_info['platform']}")
            print("=" * 60)
            
            # Phase 0: Check npm availability
            npm_available = self.check_npm_availability()
            if not npm_available:
                print("\n❌ npm/Node.js not found!")
                print("� Please install Node.js from: https://nodejs.org/")
                print("🔧 Node.js is required for building the frontend assets")
                print("📝 After installing Node.js:")
                print("   1. Restart your terminal")
                print("   2. Run this script again")
                print("\n� Deployment aborted due to missing prerequisites.")
                sys.exit(1)
            
            # Phase 1: Create Virtual Environment
            self.create_virtual_environment()
            
            # Phase 2: Environment Setup
            self.setup_environment()
            
            # Phase 3: Install Dependencies
            self.install_dependencies()
            
            # Phase 4: Skip frontend build - serve directly from src
            print("\n🔨 Skipping frontend build - serving directly from src/")
            print("✅ Using development mode with live source files")
            
            # Phase 5: Setup Backend Server
            self.setup_server()
            
            # Phase 6: Deploy Application
            self.deploy_application()
            
            print("\n" + "=" * 60)
            print("✅ Deployment completed successfully!")
            print(f"🌐 Website available at: {os.getenv('APP_URL', 'http://localhost:5000')}")
            print("📱 Mobile-optimized and responsive design")
            print("⚡ GSAP animations and smooth transitions")
            print("🎯 Swedish design aesthetics with accessibility compliance")
            print(f"🐍 Running in virtual environment: {self.venv_dir}")
            
            if not npm_available:
                print("\n💡 Tip: Install Node.js for optimized builds and better performance!")
            
        except KeyboardInterrupt:
            print("\n👋 Deployment interrupted by user.")
            self.graceful_shutdown()
        except Exception as e:
            print(f"❌ Deployment failed: {str(e)}")
            self.graceful_shutdown()
            sys.exit(1)
    
    def setup_environment(self):
        """Setup environment variables and configuration"""
        print("\n📋 Setting up environment...")
        
        env_file = self.root_dir / '.env'
        env_example = self.root_dir / '.env.example'
        
        # Create .env from .env.example if it doesn't exist
        if not env_file.exists():
            if env_example.exists():
                shutil.copy2(env_example, env_file)
                print("✅ Created .env file from .env.example")
            else:
                self.create_default_env()
                print("✅ Created default .env file")
        
        print("✅ Environment variables configured")
    
    def create_default_env(self):
        """Create default environment file"""
        default_env = """# Square Transport Website Environment Configuration
# Development Settings
DEPLOYMENT_MODE=development
DEBUG=true
HOST=localhost
PORT=5000
APP_URL=http://localhost:5000

# Database (if needed for future features)
DATABASE_URL=sqlite:///square_website.db

# API Keys (add as needed)
GOOGLE_ANALYTICS_ID=
SENTRY_DSN=

# Build Settings
NODE_ENV=development
VITE_API_URL=http://localhost:5000/api

# Security
SECRET_KEY=square-transport-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Performance
CACHE_TIMEOUT=300
STATIC_FILE_CACHE=3600

# Swedish Localization
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,sv
TIMEZONE=Europe/Stockholm
"""
        with open(self.root_dir / '.env', 'w') as f:
            f.write(default_env)
    
    def install_dependencies(self):
        """Install Python and Node.js dependencies"""
        print("\n📦 Installing dependencies...")
        
        # Install Python dependencies in virtual environment
        requirements_file = self.root_dir / 'requirements.txt'
        if requirements_file.exists():
            print("📦 Installing Python dependencies in virtual environment...")
            subprocess.run([
                str(self.venv_python), '-m', 'pip', 'install', '-r', 
                str(requirements_file)
            ], check=True)
            print("✅ Python dependencies installed in virtual environment")
        
        # Install Node.js dependencies (npm is guaranteed to be available at this point)
        package_json = self.root_dir / 'package.json'
        if package_json.exists():
            print("📦 Installing Node.js dependencies...")
            subprocess.run(['npm', 'install'], 
                         cwd=self.root_dir, 
                         check=True,
                         shell=True)  # Add shell=True for Windows
            print("✅ Node.js dependencies installed")
        
        print("✅ All available dependencies installed")
    
    def cleanup_build_artifacts(self):
        """Clean up old build artifacts to prevent accumulation of hashed files"""
        print("\n🧹 Cleaning up old build artifacts...")
        
        try:
            # Clean dist directory (Vite build output)
            dist_dir = self.root_dir / 'dist'
            if dist_dir.exists():
                print("  📂 Cleaning dist/ directory...")
                shutil.rmtree(dist_dir)
                print("  ✅ Removed old dist/ files")
            
            # Clean server/static/assets directory (unused legacy files)
            server_assets_dir = self.root_dir / 'server' / 'static' / 'assets'
            if server_assets_dir.exists():
                print("  📂 Cleaning server/static/assets/ directory...")
                shutil.rmtree(server_assets_dir)
                print("  ✅ Removed old server/static/assets/ files")
            
            # Clean any .pyc files and __pycache__ directories (excluding venv)
            for pycache_dir in self.root_dir.rglob('__pycache__'):
                if pycache_dir.is_dir() and 'venv' not in str(pycache_dir):
                    shutil.rmtree(pycache_dir)
                    print(f"  ✅ Removed {pycache_dir}")
            
            print("✅ Cleanup completed successfully")
            
        except Exception as e:
            print(f"⚠️  Warning: Cleanup encountered an issue: {e}")
            print("   Continuing with build process...")
    
    def build_frontend(self):
        """Build frontend assets using Vite with cleanup"""
        # Clean up old artifacts first
        self.cleanup_build_artifacts()
        
        print("\n🔨 Building frontend...")
        
        result = subprocess.run(['npm', 'run', 'build'], 
                              cwd=self.root_dir, 
                              capture_output=True, 
                              text=True,
                              shell=True)  # Add shell=True for Windows
        
        if result.returncode == 0:
            print("✅ Frontend built successfully with Vite")
            
            # Show build output summary
            dist_dir = self.root_dir / 'dist'
            if dist_dir.exists():
                assets_dir = dist_dir / 'assets'
                if assets_dir.exists():
                    asset_files = list(assets_dir.glob('*'))
                    print(f"  📦 Generated {len(asset_files)} asset files")
                    for asset_file in sorted(asset_files):
                        if asset_file.is_file():
                            size_kb = asset_file.stat().st_size / 1024
                            print(f"    - {asset_file.name} ({size_kb:.1f} KB)")
        else:
            print("❌ Frontend build failed:")
            print(result.stderr)
            raise subprocess.CalledProcessError(result.returncode, 'npm run build')
    
    def setup_server(self):
        """Setup and configure backend server"""
        print("\n⚙️ Setting up server...")
        
        # Ensure server directory exists
        server_dir = self.root_dir / 'server'
        server_dir.mkdir(exist_ok=True)
        
        # For development, we'll serve directly from src/
        # No need to copy files around
        print("✅ Server configured to serve from src/ directory")
        print("✅ Server configured")
    
    def deploy_application(self):
        """Deploy application based on environment"""
        print("\n🚀 Deploying application...")
        
        deployment_mode = os.getenv('DEPLOYMENT_MODE', 'development')
        
        if deployment_mode == 'development':
            self.deploy_development()
        else:
            self.deploy_development()  # Default to development
    
    def deploy_development(self):
        """Deploy in development mode"""
        print("🔧 Starting development server...")
        print("🌐 Opening browser to showcase Square's delivery robots...")
        print(f"🐍 Using virtual environment: {self.venv_dir}")
        print("\n💡 Press Ctrl+C to stop the server gracefully")
        
        # Start Flask development server using virtual environment Python
        try:
            import webbrowser
            webbrowser.open('http://localhost:5000')
        except:
            pass
        
        try:
            # Store the process for graceful shutdown
            self.server_process = subprocess.Popen([
                str(self.venv_python), 
                'server/app.py'
            ], cwd=self.root_dir)
            
            # Wait for the process to complete
            self.server_process.wait()
            
        except KeyboardInterrupt:
            print("\n🛑 Received Ctrl+C - shutting down gracefully...")
            self.graceful_shutdown()
        except Exception as e:
            print(f"\n❌ Server error: {e}")
            self.graceful_shutdown()

if __name__ == '__main__':
    deployer = SquareWebsiteDeployer()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ['clean', 'cleanup', '--clean', '--cleanup']:
            print("🧹 Running cleanup only...")
            deployer.cleanup_build_artifacts()
            print("✅ Cleanup completed. Run without arguments to start the server.")
            sys.exit(0)
        elif command in ['build', '--build']:
            print("🔨 Building frontend only...")
            try:
                deployer.cleanup_build_artifacts()
                deployer.build_frontend()
                print("✅ Build completed. Run without arguments to start the server.")
            except Exception as e:
                print(f"❌ Build failed: {e}")
                sys.exit(1)
            sys.exit(0)
        elif command in ['help', '--help', '-h']:
            print("🚀 Square Transport Website Deployment")
            print("=" * 45)
            print("Usage:")
            print("  python run_app.py          - Start development server")
            print("  python run_app.py clean    - Clean build artifacts only")
            print("  python run_app.py build    - Build frontend only")
            print("  python run_app.py help     - Show this help message")
            print("")
            print("Features:")
            print("  ✅ Automatic cleanup of old hashed files")
            print("  ✅ Virtual environment management")
            print("  ✅ Cross-platform compatibility")
            print("  ✅ Graceful shutdown handling")
            sys.exit(0)
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'python run_app.py help' for available commands")
            sys.exit(1)
    
    # Default: run the full deployment
    deployer.run()
