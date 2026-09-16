from datetime import datetime

from app.extensions import db


class HoraExtra(db.Model):

    __tablename__ = "horas_extras"


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


    latitud = db.Column(
        db.Float,
        nullable=True
    )


    longitud = db.Column(
        db.Float,
        nullable=True
    )


    direccion = db.Column(
        db.String(500),
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
        backref=db.backref(
            "horas_extras",
            lazy=True
        )
    )
