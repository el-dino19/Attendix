from app.models.jornada import Jornada
from app.models.hora_extra import HoraExtra
from app.models.descanso import Descanso


def obtener_historial_usuario(usuario_id):

    jornadas = Jornada.query.filter(
        Jornada.usuario_id == usuario_id
    ).order_by(
        Jornada.fecha.desc()
    ).all()

    historial = []

    for jornada in jornadas:

        # =================================================
        # HORAS EXTRAS DE ESTA JORNADA
        # =================================================

        hora_extra = HoraExtra.query.filter(
            HoraExtra.jornada_id == jornada.id
        ).order_by(
            HoraExtra.inicio.desc()
        ).first()

        # =================================================
        # DESCANSOS
        # =================================================

        descansos = Descanso.query.filter(
            Descanso.jornada_id == jornada.id
        ).order_by(
            Descanso.inicio.asc()
        ).all()

        # =================================================
        # REGISTRO
        # =================================================

        historial.append({
            "jornada": jornada,
            "hora_extra": hora_extra,
            "descansos": descansos
        })

    return historial
