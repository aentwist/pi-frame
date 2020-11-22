import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "deep_fried_lemons"
    UPLOADS_DEFAULT_DEST = "/var/www/pi-frame/uploads"
    RESULTS_PER_PAGE = 12
    FRAME_USERNAME = "pi"
    FRAME_HOST = "192.168.1.31"


class DevConfig(Config):
    pass


class TestConfig(Config):
    pass


class ProdConfig(Config):
    pass
