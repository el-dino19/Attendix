from datetime import datetime, timedelta

from app.extensions import db
from app.models import Jornada
from app.services.correo import enviar_recordatorio


def revisar_jornadas():

    ahora = datetime.now()

    jornadas = Jornada.query.filter(
        Jornada.salida.is_(None),
        Jornada.correo_recordatorio.is_(False)
    ).all()

    for jornada in jornadas:

        inicio = datetime.combine(
            jornada.fecha,
            jornada.entrada
        )

        limite = inicio + timedelta(hours=8)

        if ahora >= limite:

            enviar_recordatorio(
                jornada.usuario.nombre,
                jornada.usuario.correo
            )

            jornada.correo_recordatorio = True

    db.session.commit()
