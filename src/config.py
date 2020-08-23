import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "deep_fried_lemons"
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


class DevConfig(Config):
    UPLOAD_FOLDER = "/var/www/full-frame/uploads"


class TestConfig(Config):
    false


class ProdConfig(Config):
    UPLOAD_FOLDER = "/mnt/hdd/shared"
