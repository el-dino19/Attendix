from datetime import datetime

from app.extensions import db


class Grupo(db.Model):
    __tablename__ = "grupos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    nombre = db.Column(db.String(120), nullable=False, unique=True)

    descripcion = db.Column(db.String(500), nullable=True)

    activo = db.Column(db.Boolean, nullable=False, default=True)

    creado_por = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
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

    creador = db.relationship(
        "Usuario",
        foreign_keys=[creado_por],
        backref="grupos_creados"
    )

    miembros = db.relationship(
        "GrupoMiembro",
        back_populates="grupo",
        cascade="all, delete-orphan",
        lazy=True
    )

    jornadas = db.relationship(
        "Jornada",
        back_populates="grupo",
        lazy=True
    )

    horas_extras = db.relationship(
        "HoraExtra",
        back_populates="grupo",
        lazy=True
    )
