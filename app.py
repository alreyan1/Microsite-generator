import os
import json
import zipfile
import shutil
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///microsites.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)

# Database Models
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tagline = db.Column(db.String(200))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    facebook = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    logo_path = db.Column(db.String(200))
    theme = db.Column(db.String(50), default='minimal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='business', lazy=True, cascade='all, delete-orphan')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper functions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_business_name(name):
    """Convert business name to safe folder name"""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name.lower().strip())

def resize_image(image_path, max_size=(800, 600)):
    """Resize image to fit within max_size while maintaining aspect ratio"""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(image_path, optimize=True, quality=85)
    except Exception as e:
        print(f"Error resizing image: {e}")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_microsite():
    try:
        # Get business information
        business_name = request.form.get('business_name', '').strip()
        if not business_name:
            flash('Business name is required!', 'error')
            return redirect(url_for('index'))
            
        tagline = request.form.get('tagline', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        facebook = request.form.get('facebook', '')
        instagram = request.form.get('instagram', '')
        twitter = request.form.get('twitter', '')
        theme = request.form.get('theme', 'minimal')

        # Handle logo upload
        logo_path = None
        if 'logo' in request.files:
            logo_file = request.files['logo']
            if logo_file.filename != '' and allowed_file(logo_file.filename):
                filename = secure_filename(f"{sanitize_business_name(business_name)}_logo_{logo_file.filename}")
                logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                logo_file.save(logo_path)
                resize_image(logo_path, (400, 300))

        # Create business record
        business = Business(
            name=business_name,
            tagline=tagline,
            email=email,
            phone=phone,
            address=address,
            facebook=facebook,
            instagram=instagram,
            twitter=twitter,
            logo_path=logo_path,
            theme=theme
        )
        db.session.add(business)
        db.session.flush()  # Get the ID

        # Handle products
        product_names = request.form.getlist('product_name')
        product_prices = request.form.getlist('product_price')
        product_descriptions = request.form.getlist('product_description')
        product_images = request.files.getlist('product_image')

        # Check if at least one product is provided
        has_valid_product = any(name.strip() for name in product_names)
        if not has_valid_product:
            flash('At least one product is required!', 'error')
            return redirect(url_for('index'))

        for i, name in enumerate(product_names):
            if name.strip():  # Only add products with names
                try:
                    price = float(product_prices[i]) if i < len(product_prices) and product_prices[i] else 0.0
                except (ValueError, IndexError):
                    price = 0.0
                description = product_descriptions[i] if i < len(product_descriptions) else ''
                
                # Handle product image
                image_path = None
                if i < len(product_images) and product_images[i].filename != '':
                    if allowed_file(product_images[i].filename):
                        filename = secure_filename(f"{sanitize_business_name(business_name)}_product_{i}_{product_images[i].filename}")
                        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        product_images[i].save(image_path)
                        resize_image(image_path, (600, 400))

                product = Product(
                    business_id=business.id,
                    name=name,
                    price=price,
                    description=description,
                    image_path=image_path
                )
                db.session.add(product)

        db.session.commit()

        # Generate the microsite
        generate_microsite(business)

        flash('Microsite created successfully!', 'success')
        return redirect(url_for('preview_microsite', business_name=sanitize_business_name(business_name)))

    except Exception as e:
        db.session.rollback()
        flash(f'Error creating microsite: {str(e)}', 'error')
        return redirect(url_for('index'))

def generate_microsite(business):
    """Generate static HTML files for the microsite"""
    try:
        safe_name = sanitize_business_name(business.name)
        microsite_dir = os.path.join('sites', safe_name)
        
        print(f"Generating microsite for {business.name} with theme {business.theme}")
        
        # Create microsite directory
        os.makedirs(microsite_dir, exist_ok=True)
        os.makedirs(os.path.join(microsite_dir, 'assets'), exist_ok=True)
        os.makedirs(os.path.join(microsite_dir, 'images'), exist_ok=True)

        # Copy logo and product images
        if business.logo_path and os.path.exists(business.logo_path):
            shutil.copy2(business.logo_path, os.path.join(microsite_dir, 'images', 'logo.jpg'))
        
        for i, product in enumerate(business.products):
            if product.image_path and os.path.exists(product.image_path):
                ext = os.path.splitext(product.image_path)[1]
                shutil.copy2(product.image_path, os.path.join(microsite_dir, 'images', f'product_{i}{ext}'))

        # Generate HTML files
        theme_base = f'microsite_themes/{business.theme}'
        print(f"Using theme base: {theme_base}")
        
        # Check if theme templates exist
        theme_templates = [
            f'{theme_base}/index.html',
            f'{theme_base}/products.html', 
            f'{theme_base}/about.html',
            f'{theme_base}/style.css'
        ]
        
        for template in theme_templates:
            template_path = os.path.join('templates', template)
            if not os.path.exists(template_path):
                raise Exception(f"Template not found: {template_path}")
        
        # Homepage
        homepage_html = render_template(f'{theme_base}/index.html', business=business)
        with open(os.path.join(microsite_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(homepage_html)
        
        # Products page
        products_html = render_template(f'{theme_base}/products.html', business=business)
        with open(os.path.join(microsite_dir, 'products.html'), 'w', encoding='utf-8') as f:
            f.write(products_html)
        
        # About page
        about_html = render_template(f'{theme_base}/about.html', business=business)
        with open(os.path.join(microsite_dir, 'about.html'), 'w', encoding='utf-8') as f:
            f.write(about_html)
        
        # Copy CSS file
        css_content = render_template(f'{theme_base}/style.css', business=business)
        with open(os.path.join(microsite_dir, 'assets', 'style.css'), 'w', encoding='utf-8') as f:
            f.write(css_content)
            
        print(f"Microsite generated successfully at {microsite_dir}")
        
    except Exception as e:
        print(f"Error in generate_microsite: {str(e)}")
        raise e

@app.route('/preview/<business_name>')
def preview_microsite(business_name):
    microsite_dir = os.path.join('sites', business_name)
    if not os.path.exists(microsite_dir):
        flash('Microsite not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('preview.html', business_name=business_name)

@app.route('/sites/<business_name>/')
@app.route('/sites/<business_name>/<path:filename>')
def serve_microsite(business_name, filename='index.html'):
    microsite_dir = os.path.join('sites', business_name)
    return send_file(os.path.join(microsite_dir, filename))

@app.route('/test-flash')
def test_flash():
    flash('This is a test success message!', 'success')
    flash('This is a test error message!', 'error')
    return redirect(url_for('index'))

@app.route('/debug-form', methods=['GET', 'POST'])
def debug_form():
    if request.method == 'POST':
        data = {
            'business_name': request.form.get('business_name'),
            'products': request.form.getlist('product_name'),
            'theme': request.form.get('theme')
        }
        flash(f'Form data received: {data}', 'success')
        return redirect(url_for('index'))
    
    return '''
    <form method="POST">
        <input name="business_name" placeholder="Business Name" required><br><br>
        <input name="product_name" placeholder="Product 1"><br><br>
        <select name="theme">
            <option value="minimal">Minimal</option>
            <option value="modern">Modern</option>
            <option value="fancy">Fancy</option>
        </select><br><br>
        <button type="submit">Test Submit</button>
    </form>
    '''

@app.route('/download/<business_name>')
def download_microsite(business_name):
    microsite_dir = os.path.join('sites', business_name)
    if not os.path.exists(microsite_dir):
        flash('Microsite not found', 'error')
        return redirect(url_for('index'))
    
    # Create zip file
    zip_path = f"{business_name}_microsite.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(microsite_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, microsite_dir)
                zipf.write(file_path, arcname)
    
    return send_file(zip_path, as_attachment=True, download_name=f"{business_name}_microsite.zip")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5001, debug=True)