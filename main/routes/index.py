from flask import Blueprint, current_app


index_bp = Blueprint('index', __name__, url_prefix='/engines/pspack')


@index_bp.route('/')
def index():
    return current_app.engine.index()


@index_bp.route('/liveness')
def liveness():
    return current_app.engine.liveness()


@index_bp.route('/readiness')
def readiness():
    return current_app.engine.readiness()


@index_bp.route("/test")
def test():
    """Return test page."""
    return current_app.engine.test()


@index_bp.route("/info")
def info():
    """Get info on running engine."""
    return current_app.engine.info()
