from flask import Flask
from config import Config
from app.models import db, ma
from app.services.auth_service import AuthService

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create superadmin
        AuthService.create_superadmin()

    # Import and register blueprints
    from app.routes.admin_routes import admin_bp
    from app.routes.teacher_routes import teacher_bp
    from app.routes.student_routes import student_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(student_bp, url_prefix='/student')

    return app