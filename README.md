# Square Transport Website

![Square Transport](src/assets/images/logo%20NEW1%20BW%201.png)

A modern, responsive website for Square Transport, a Swedish startup revolutionizing urban delivery with AI-powered autonomous robots.

## 🚀 About Square Transport

Square Transport is pioneering the future of last-mile delivery through innovative AI-driven autonomous delivery robots. Our mission is to create efficient, sustainable, and reliable delivery solutions for urban environments.

### Key Features
- **AI-Powered Delivery**: Advanced autonomous robots for safe and efficient deliveries
- **Swedish Innovation**: Cutting-edge technology from Sweden's startup ecosystem
- **Sustainable Solutions**: Eco-friendly delivery alternatives for modern cities
- **Real-time Tracking**: Advanced monitoring and optimization systems

## 🛠️ Tech Stack

### Frontend
- **Vite** - Fast build tool and development server
- **HTML5/CSS3** - Modern web standards
- **JavaScript (ES6+)** - Interactive functionality
- **GSAP** - High-performance animations
- **Framer Motion** - React animation library

### Backend
- **Flask** - Lightweight Python web framework
- **Python 3.8+** - Server-side logic
- **Gunicorn** - Production WSGI server

### Deployment
- **GoDaddy** - Web hosting platform
- **FTP** - File transfer for deployment
- **Automated Scripts** - One-click deployment solutions

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16.x or higher
- Git

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bvspa003/Square.git
   cd Square
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies**
   ```bash
   npm install
   ```

## 🏃‍♂️ Usage

### Development

1. **Start the Flask server**
   ```bash
   python run_app.py
   ```

2. **In another terminal, start the Vite dev server**
   ```bash
   npm run dev
   ```

3. **Open your browser** and navigate to `http://localhost:5000`

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## 📁 Project Structure

```
Square/
├── server/                 # Flask backend
│   └── app.py             # Main Flask application
├── src/                   # Frontend source files
│   ├── assets/           # Images, fonts, icons
│   ├── pages/            # HTML pages
│   ├── scripts/          # JavaScript files
│   └── styles/           # CSS stylesheets
├── data/                  # Company data and assets
├── dist/                  # Built production files
├── deploy_godaddy.py      # GoDaddy deployment script
├── run_app.py            # Local development runner
└── package.json          # Node.js dependencies
```

## 🚀 Deployment

### Automated GoDaddy Deployment

1. **Configure environment variables**
   Create a `.env` file with your GoDaddy FTP credentials:
   ```
   GODADDY_HOST=your-hostname
   GODADDY_USER=your-username
   GODADDY_PASS=your-password
   ```

2. **Run deployment script**
   ```bash
   python deploy_godaddy.py
   ```

### Manual Deployment

1. Build the project:
   ```bash
   npm run build
   ```

2. Upload the `dist/` folder contents to your web server

## 📊 API Endpoints

- `GET /` - Landing page
- `GET /overview` - Product overview
- `GET /about` - Company information
- `GET /api/company-data` - Company data (JSON)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Square Transport Team
- Website: [Coming Soon]
- Email: info@square-transport.com
- LinkedIn: [Company Profile]

---

*Built with ❤️ by the Square Transport team*
