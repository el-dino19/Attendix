from app.extensions import db
from datetime import datetime


class Jornada(db.Model):
    __tablename__ = "jornadas"

    id = db.Column(
        db.BigInteger,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    fecha = db.Column(
        db.Date,
        nullable=False
    )

    entrada = db.Column(
    db.Time,
    nullable=False
)

    salida = db.Column(
        db.Time,
        nullable=True
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

    usuario = db.relationship(
        "Usuario",
        back_populates="jornadas"
    )

    descansos = db.relationship(
        "Descanso",
        back_populates="jornada",
        cascade="all, delete-orphan"
    )