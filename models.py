from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, FloatField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///furniture.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
admin = Admin(app, name="Admin Panel", template_mode="bootstrap3")
login_manager = LoginManager(app)

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Furniture Model
class Furniture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)  # Image storage

# Furniture Form
class FurnitureForm(FlaskForm):
    name = StringField('Furniture Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    image = FileField('Furniture Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Upload')

# Add an unrestricted view (anyone with admin panel access can modify furniture)
admin.add_view(ModelView(Furniture, db.session))

if __name__ == "__main__":
    app.run(debug=True)

