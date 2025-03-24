import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload Configurations
    UPLOAD_FOLDER = "static/images"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # Ensure the upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    @staticmethod
    def allowed_file(filename):
        """Check if the uploaded file is allowed."""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///furniture.db"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///furniture.db")

# Dictionary to easily switch environments
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}



