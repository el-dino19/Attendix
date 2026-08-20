from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from app.models import Usuario, Jornada, Descanso

    # ========================
    # REGISTRO DE RUTAS
    # ========================
    
    
    from app.routes.auth import auth_bp
    from app.routes.empleado import empleado_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(empleado_bp)
    app.register_blueprint(admin_bp)

    return app