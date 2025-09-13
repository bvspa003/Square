#!/usr/bin/env python3
"""
Square Transport Website - Flask Backend Server
Serves the website and provides API endpoints for dynamic content
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, send_from_directory, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'square-transport-secret')
app.config['DEBUG'] = os.getenv('DEBUG', 'true').lower() == 'true'

# Get the root directory
ROOT_DIR = Path(__file__).parent.parent
STATIC_DIR = ROOT_DIR / 'src'  # Serve directly from src during development
DATA_DIR = ROOT_DIR / 'data'

@app.route('/')
def index():
    """Landing page - showcase Square's delivery robots"""
    return send_from_directory(STATIC_DIR / 'pages', 'index.html')

@app.route('/overview')
def overview():
    """Overview page - detailed product information"""
    return send_from_directory(STATIC_DIR / 'pages', 'overview.html')

@app.route('/about')
def about():
    """About page - team and company information"""
    return send_from_directory(STATIC_DIR / 'pages', 'about.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory(STATIC_DIR, filename)

@app.route('/assets/<path:filename>')
def asset_files(filename):
    """Serve asset files"""
    return send_from_directory(STATIC_DIR / 'assets', filename)

@app.route('/styles/<path:filename>')
def style_files(filename):
    """Serve CSS files"""
    return send_from_directory(STATIC_DIR / 'styles', filename)

@app.route('/scripts/<path:filename>')
def script_files(filename):
    """Serve JavaScript files"""
    return send_from_directory(STATIC_DIR / 'scripts', filename)

@app.route('/api/company-data')
def get_company_data():
    """API endpoint to get company data"""
    try:
        # Read problem statement
        problem_file = DATA_DIR / 'Problem statement.txt'
        problem_statement = ""
        if problem_file.exists():
            with open(problem_file, 'r', encoding='utf-8') as f:
                problem_statement = f.read()
        
        # Read links
        links_file = DATA_DIR / 'links.txt'
        links_data = ""
        if links_file.exists():
            with open(links_file, 'r', encoding='utf-8') as f:
                links_data = f.read()
        
        # Process achievements from links
        achievements = []
        team_members = []
        
        for line in links_data.split('\n'):
            if 'innovatumsciencepark.se' in line:
                achievements.append({
                    'title': 'Winner - Startup Challenge',
                    'description': 'Square wins Startup Challenge with AI-based delivery robots',
                    'url': line.strip()
                })
            elif 'linkedin.com/in/' in line and 'Founder' in line:
                team_members.append({
                    'role': 'Founder',
                    'url': line.split()[0]
                })
        
        return jsonify({
            'problem_statement': problem_statement,
            'achievements': achievements,
            'team_members': team_members,
            'market_data': {
                'total_addressable_market': '$500M',
                'serviceable_addressable_market': '$200M',
                'serviceable_obtainable_market': '$15M'
            },
            'benefits': {
                'cost_reduction': '70%',
                'energy_reduction': '80%',
                'carbon_reduction': '90%'
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Square Transport Website',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    host = os.getenv('HOST', 'localhost')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    print(f"🚀 Starting Square Transport Website Server")
    print(f"🌐 Server running at: http://{host}:{port}")
    print(f"📱 Mobile-optimized responsive design")
    print(f"⚡ GSAP animations and smooth interactions")
    print(f"🎯 Swedish design aesthetics")
    
    app.run(host=host, port=port, debug=debug)
