import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "deep_fried_lemons"
    UPLOADS_DEFAULT_DEST = "/var/www/full-frame/uploads"
    RESULTS_PER_PAGE = 12


class DevConfig(Config):
    pass


class TestConfig(Config):
    pass


class ProdConfig(Config):
    pass
