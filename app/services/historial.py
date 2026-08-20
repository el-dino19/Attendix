from app.models.jornada import Jornada
from app.models.descanso import Descanso


def obtener_historial_usuario(usuario_id):

    jornadas = Jornada.query.filter(
        Jornada.usuario_id == usuario_id
    ).order_by(
        Jornada.fecha.desc(),
        Jornada.entrada.desc()
    ).all()

    historial = []

    for jornada in jornadas:

        descansos = Descanso.query.filter(
            Descanso.jornada_id == jornada.id
        ).order_by(
            Descanso.inicio.asc()
        ).all()

        historial.append({
            "jornada": jornada,
            "descansos": descansos
        })

    return historial