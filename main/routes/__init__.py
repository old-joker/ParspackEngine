from flask import Flask
from config import load_config
from routes.error_handlers import register_error_handlers
from .index import index_bp
from .scan import scan_bp
from .report import report_bp
from .status import status_bp
from .clean import clean_bp
from .findings import findings_bp
from PatrowlEnginesUtils.PatrowlEngine import PatrowlEngine
from utils.constants import APP_BASE_DIR, APP_ENGINE_NAME
from flask_celeryext import FlaskCeleryExt


def create_app():
    app = Flask(__name__)

    load_config(app)

    # Setup Celery Extention
    ext_celery = FlaskCeleryExt()
    ext_celery.init_app(app)

    engine = PatrowlEngine(
        app=app, base_dir=APP_BASE_DIR, name=APP_ENGINE_NAME
    )

    # Attach the engine to app (accessible in other routes via current_app)
    app.engine = engine

    # Register all route blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(scan_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(clean_bp)
    app.register_blueprint(findings_bp)

    # Register error handlers
    register_error_handlers(app)

    return app, ext_celery.celery
