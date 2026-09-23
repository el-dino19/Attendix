from datetime import datetime

from app.extensions import db


class GrupoMiembro(db.Model):
    __tablename__ = "grupo_miembros"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    grupo_id = db.Column(
        db.Integer,
        db.ForeignKey("grupos.id", ondelete="CASCADE"),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    rol = db.Column(
        db.String(20),
        nullable=False,
        default="colaborador"
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

    grupo = db.relationship(
        "Grupo",
        back_populates="miembros"
    )

    usuario = db.relationship(
        "Usuario",
        back_populates="grupos_miembro"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "grupo_id",
            "usuario_id",
            name="uq_grupo_miembro"
        ),
    )
