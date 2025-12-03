# E-commerce Microsite Generator

A powerful Flask web application that allows users to create beautiful, responsive e-commerce microsites in minutes. Choose from multiple themes, add business information and products, and generate complete websites ready for deployment.

## Features

### ✨ Core Features
- **Easy-to-use web interface** - Create microsites through a simple form
- **Multiple themes** - Choose from Minimal, Modern, and Fancy designs
- **Business information** - Add company details, contact info, and social links
- **Product management** - Add multiple products with images, prices, and descriptions
- **Logo upload** - Upload and display your business logo
- **Image handling** - Automatic image resizing and optimization
- **Live preview** - See your microsite before downloading
- **ZIP download** - Get your complete microsite as a downloadable file

### 🎨 Available Themes
1. **Minimal** - Clean, simple design focused on content
2. **Modern** - Bold, contemporary style with gradients and modern typography
3. **Fancy** - Elegant, luxury design with gold accents and premium fonts

### 📱 Responsive Design
All generated microsites are fully responsive and work perfectly on:
- Desktop computers
- Tablets
- Mobile phones

## Project Structure

```
site generator/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── test_app.py                    # Test script
├── microsites.db                  # SQLite database (created automatically)
├── templates/
│   ├── index.html                 # Homepage form
│   ├── preview.html               # Preview page
│   └── microsite_themes/
│       ├── minimal/               # Minimal theme templates
│       ├── modern/                # Modern theme templates
│       └── fancy/                 # Fancy theme templates
├── static/
│   ├── css/
│   │   └── main.css              # Main application styles
│   ├── js/
│   │   └── main.js               # Interactive form functionality
│   └── uploads/                   # Uploaded images storage
└── sites/                         # Generated microsites
    └── {business_name}/           # Individual microsite folders
        ├── index.html
        ├── products.html
        ├── about.html
        ├── assets/
        │   └── style.css
        └── images/
            ├── logo.jpg
            └── product_*.jpg
```

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd "/Users/muhammadusafbaig/site generator"
   ```

2. **Install dependencies:**
   ```bash
   "/Users/muhammadusafbaig/site generator/.venv/bin/python" -m pip install -r requirements.txt
   ```

3. **Run the test script to verify setup:**
   ```bash
   "/Users/muhammadusafbaig/site generator/.venv/bin/python" test_app.py
   ```

4. **Start the application:**
   ```bash
   "/Users/muhammadusafbaig/site generator/.venv/bin/python" app.py
   ```

5. **Open your browser and visit:**
   ```
   http://127.0.0.1:5000
   ```

## Usage Guide

### Creating a Microsite

1. **Fill in Business Information:**
   - Business Name (required)
   - Tagline
   - Contact details (email, phone, address)
   - Upload logo image

2. **Add Social Media Links:**
   - Facebook
   - Instagram
   - Twitter

3. **Add Products:**
   - Product Name (required)
   - Price
   - Description
   - Product Image
   - Use the "Add Product" button to add multiple products

4. **Choose a Theme:**
   - **Minimal**: Clean and simple
   - **Modern**: Bold and contemporary
   - **Fancy**: Elegant and luxurious

5. **Generate Microsite:**
   - Click "Generate My Microsite"
   - Wait for processing
   - Get redirected to preview page

### Preview and Download

1. **Preview**: View your microsite in an embedded frame
2. **Download**: Click "Download ZIP" to get your complete microsite
3. **Host Anywhere**: Extract the ZIP file and upload to any web hosting service

## Technical Details

### Dependencies
- **Flask 2.3.3** - Web framework
- **Flask-SQLAlchemy 3.0.5** - Database ORM
- **Werkzeug 2.3.7** - WSGI utilities
- **Jinja2 3.1.2** - Template engine
- **Pillow 10.0.1** - Image processing

### Database Schema

**Business Table:**
- Business information and settings
- Logo path and theme selection
- Social media links

**Product Table:**
- Product details linked to businesses
- Image paths and pricing
- Descriptions

### File Upload Handling
- Secure filename generation
- Image resizing and optimization
- Support for PNG, JPG, GIF, WebP formats
- Automatic file organization

### Microsite Generation
- Dynamic HTML generation using Jinja2
- Theme-specific CSS and layouts
- Static asset copying
- SEO-friendly structure

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Homepage with creation form |
| `/create` | POST | Process form and generate microsite |
| `/preview/<business_name>` | GET | Preview generated microsite |
| `/sites/<business_name>/` | GET | Serve microsite files |
| `/download/<business_name>` | GET | Download microsite as ZIP |

## Customization

### Adding New Themes
1. Create a new directory in `templates/microsite_themes/`
2. Add `index.html`, `products.html`, `about.html`, and `style.css`
3. Update the theme selection in `templates/index.html`
4. Add theme option to the form processing in `app.py`

### Modifying Existing Themes
- Edit CSS files in theme directories
- Modify HTML templates for layout changes
- Update color schemes and typography

## Troubleshooting

### Common Issues

**Database Errors:**
- Run the test script to reinitialize the database
- Check file permissions

**Image Upload Issues:**
- Verify `static/uploads/` directory exists
- Check file size limits (16MB max)
- Ensure supported image formats

**Missing Templates:**
- Run test script to verify all files
- Check directory structure

**Theme Not Applying:**
- Verify theme directory structure
- Check CSS file paths
- Clear browser cache

### Getting Help
1. Run the test script for diagnostics
2. Check the console for error messages
3. Verify all required files exist

## Production Deployment

### Security Considerations
- Change the Flask secret key
- Use environment variables for configuration
- Set up proper file permissions
- Use a production WSGI server (Gunicorn, uWSGI)

### Performance Optimization
- Use a reverse proxy (Nginx)
- Implement caching
- Optimize image sizes
- Use CDN for static assets

## License

This project is open source and available under the MIT License.

## Credits

Built with:
- Flask (Python web framework)
- Bootstrap (CSS framework)
- Font Awesome (Icons)
- Google Fonts (Typography)

---

**Happy microsite building! 🚀**