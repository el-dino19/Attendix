from app.extensions import db
from datetime import datetime


class HoraExtra(db.Model):

    __tablename__ = "horas_extras"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    jornada_id = db.Column(
        db.BigInteger,
        db.ForeignKey(
            "jornadas.id",
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuarios.id",
            onupdate="CASCADE"
        ),
        nullable=False
    )

    inicio = db.Column(
        db.DateTime,
        nullable=False
    )

    fin = db.Column(
        db.DateTime,
        nullable=True
    )

    latitud_inicio = db.Column(
        db.Numeric(10, 8),
        nullable=True
    )

    longitud_inicio = db.Column(
        db.Numeric(11, 8),
        nullable=True
    )

    ubicacion_inicio = db.Column(
        db.String(255),
        nullable=True
    )

    latitud_fin = db.Column(
        db.Numeric(10, 8),
        nullable=True
    )

    longitud_fin = db.Column(
        db.Numeric(11, 8),
        nullable=True
    )

    ubicacion_fin = db.Column(
        db.String(255),
        nullable=True
    )

    minutos_totales = db.Column(
        db.Integer,
        nullable=True
    )

    estado = db.Column(
        db.Enum(
            "activa",
            "finalizada",
            "cancelada"
        ),
        nullable=False,
        default="activa"
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
        back_populates="horas_extras"
    )

    jornada = db.relationship(
        "Jornada",
        back_populates="horas_extras"
    )
