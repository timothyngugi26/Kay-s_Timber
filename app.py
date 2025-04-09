import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy  # Fixed Import
from werkzeug.utils import secure_filename
from PIL import Image
from flask_migrate import Migrate

app = Flask(__name__)

UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///furniture.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
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
def admin_panel():
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

    products = Furniture.query.all()  # Fetch all products for admin panel
    return render_template("admin.html", products=products) 

@app.route("/products")
def display_products():
    products = Furniture.query.all()
    return render_template("products.html", products=products)
@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = Furniture.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form["description"]
        product.price = float(request.form["price"])

        if "file" in request.files:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(image_path)

                resize_image(image_path)

                product.image_filename = filename

        db.session.commit()
        return redirect(url_for("admin_panel"))

    return render_template("edit_product.html", product=product)

@app.route("/delete/<int:product_id>", methods=["GET", "POST"])  # Allow both methods
def delete_product(product_id):
    product = Furniture.query.get_or_404(product_id)
    
    if request.method == "POST":
        # Handle deletion
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for("display_products"))
    
    # GET request: Show confirmation page
    return render_template("delete_product.html", product=product)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True, port=10000)
