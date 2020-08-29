import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "deep_fried_lemons"
    FRAME_HOST = "pi@192.168.1.31"
    SLIDESHOW_DEFAULT_PATH = "/mnt/nas"
    RESULTS_PER_PAGE = 24


class DevConfig(Config):
    UPLOADS_DEFAULT_DEST = "/var/www/full-frame/uploads"


class TestConfig(Config):
    UPLOADS_DEFAULT_DEST = ""


class ProdConfig(Config):
    UPLOADS_DEFAULT_DEST = "/mnt/hdd/shared"
