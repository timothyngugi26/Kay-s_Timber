import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models import db, Product
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

# Define Blueprint
routes = Blueprint("routes", __name__)

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route("/admin", methods=["GET", "POST"])
def upload_image():
    """Upload product with an image."""
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")

@routes.route("/admin", methods=["REMOVE"])
def Remove_image():
    """Upload product with an image."""
    if request.method == "REMOVE":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")

        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)  # Save to static/uploads/

            # Save product to database
            new_product = Product(name=name, description=description, price=price, image=filename)
            db.session.add(new_product)
            db.session.commit()

            flash("Product uploaded successfully!")
            return redirect(url_for("routes.view_products"))

    return render_template("admin.html")

@routes.route("/products")
def view_products():
    """View all uploaded products."""
    products = Product.query.all()
    return render_template("products.html", products=products)

