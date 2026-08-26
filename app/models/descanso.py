from app.extensions import db

from datetime import datetime


class Descanso(db.Model):

    __tablename__ = "descansos"

    id = db.Column(
        db.BigInteger,
        primary_key=True
    )

    jornada_id = db.Column(
        db.BigInteger,
        db.ForeignKey("jornadas.id"),
        nullable=False
    )

    tipo = db.Column(
        db.Enum(
            "break_manana",
            "lunch",
            "break_tarde"
        ),
        nullable=False
    )

    inicio = db.Column(
        db.Time,
        nullable=False
    )

    fin = db.Column(
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

    jornada = db.relationship(
        "Jornada",
        back_populates="descansos"
    )