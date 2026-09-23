from app.models.jornada import Jornada
from app.models.hora_extra import HoraExtra
from app.models.descanso import Descanso


def obtener_historial_usuario(usuario_id, grupo_id=None):
    query = Jornada.query.filter(
        Jornada.usuario_id == usuario_id
    )

    if grupo_id is not None:
        query = query.filter(Jornada.grupo_id == grupo_id)

    jornadas = query.order_by(
        Jornada.fecha.desc()
    ).all()

    historial = []

    for jornada in jornadas:
        hora_extra = HoraExtra.query.filter(
            HoraExtra.jornada_id == jornada.id
        ).order_by(
            HoraExtra.inicio.desc()
        ).first()

        descansos = Descanso.query.filter(
            Descanso.jornada_id == jornada.id
        ).order_by(
            Descanso.inicio.asc()
        ).all()

        historial.append({
            "jornada": jornada,
            "hora_extra": hora_extra,
            "descansos": descansos
        })

    return historial
