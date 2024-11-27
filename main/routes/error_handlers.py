from flask import jsonify, current_app
from PatrowlEnginesUtils.PatrowlEngineExceptions import PatrowlEngineExceptions

def register_error_handlers(app):
    """Register error handlers for the Flask app."""
    
    @app.errorhandler(404)
    def page_not_found(e):
        """Page not found."""
        return current_app.engine.page_not_found()

    @app.errorhandler(PatrowlEngineExceptions)
    def handle_invalid_usage(error):
        """Handle PatrowlEngineExceptions and return a proper response."""
        response = jsonify(error.to_dict())
        response.status_code = 404
        return response
