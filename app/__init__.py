from flask import Flask, render_template
from config import Config
from app.extensions import db, bcrypt



def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("403.html"), 403

    from app.models import Usuario, Jornada, Descanso

    from app.routes.auth import auth_bp
    from app.routes.empleado import empleado_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(empleado_bp)
    app.register_blueprint(admin_bp)

    return app
