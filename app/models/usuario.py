from app.extensions import db
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    correo = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    rol = db.Column(
    db.String(20),
    nullable=False,
    default="empleado"
    )

    activo = db.Column(
    db.Boolean,
    nullable=False,
    default=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    jornadas = db.relationship(
        "Jornada",
        back_populates="usuario"
    )