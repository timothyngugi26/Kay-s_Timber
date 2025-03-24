import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models import Furniture
from config import config_dict
from PIL import Image

app = Flask(__name__)

# Configure upload folder and database
UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///furniture.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)

# Define Furniture model
class Furniture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)

def allowed_file(filename):
    """Check if the uploaded file is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image_path, max_width=500):
    """Resize image while maintaining aspect ratio."""
    img = Image.open(image_path)
    width, height = img.size

    if width > max_width:
        new_height = int((max_width / width) * height)
        img = img.resize((max_width, new_height))
        img.save(image_path)  # Overwrite the original image

@app.route("/")
def home():
    return render_template("index.html")  # Home Page

@app.route("/admin", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")

        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(image_path)

            # Resize the image
            resize_image(image_path)

            # Save product info to database
            new_product = Furniture(name=name, description=description, price=float(price), image_filename=filename)
            db.session.add(new_product)
            db.session.commit()

            return redirect(url_for("display_products"))

    return render_template("admin.html")  # Admin Panel

@app.route('/admin')
def admin_panel():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('admin.html', products=products) 

@app.route("/products")
def display_products():
    products = Furniture.query.all()
    return render_template("products.html", products=products)  # Display Uploaded Products

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True, port=10000)

