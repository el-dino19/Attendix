from datetime import datetime
from zoneinfo import ZoneInfo

from app import db
from app.models.jornada import Jornada


def obtener_hora_actual(zona_horaria="UTC"):

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    ahora = datetime.now(zona)

    return ahora.time()

def formatear_direccion_corta(direccion):
    """
    Genera una dirección corta para mostrar en el dashboard.

    No depende de un país o ciudad específica.
    La dirección original permanece intacta en la base de datos.
    """

    if not direccion:
        return "Ubicación no disponible"

    partes = [
        parte.strip()
        for parte in direccion.split(",")
        if parte.strip()
    ]

    # Elimina duplicados manteniendo el orden
    resultado = []

    for parte in partes:

        if parte not in resultado:
            resultado.append(parte)

    # Tomamos solamente las primeras partes relevantes.
    #
    # Como la estructura de Nominatim puede variar según el país,
    # evitamos eliminar nombres específicos como "Barranquilla",
    # "Riomar", etc.

    if len(resultado) > 6:
        resultado = resultado[:6]

    return ", ".join(resultado)



def obtener_fecha_actual(zona_horaria="UTC"):

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    ahora = datetime.now(zona)

    return ahora.date()


def obtener_jornada_abierta(usuario_id):

    jornada = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.salida.is_(None)
    ).order_by(
        Jornada.fecha.desc(),
        Jornada.entrada.desc()
    ).first()

    return jornada


def registrar_entrada(
    usuario_id,
    zona_horaria="UTC",
    latitud=None,
    longitud=None,
    direccion=None
):

    # =====================================================
    # ZONA HORARIA
    # =====================================================

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")


    # =====================================================
    # FECHA Y HORA ACTUAL
    # =====================================================

    ahora = datetime.now(zona)

    fecha_hoy = ahora.date()
    hora_actual = ahora.time()


    # =====================================================
    # VERIFICAR SI YA EXISTE JORNADA
    # =====================================================

    jornada_existente = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.fecha == fecha_hoy
    ).first()

    if jornada_existente:
        return jornada_existente


    # =====================================================
    # LIMPIAR DIRECCIÓN
    # =====================================================

    if direccion:
        direccion = direccion.strip()

    else:
        direccion = None


    # =====================================================
    # CREAR JORNADA
    # =====================================================

    jornada = Jornada(
        usuario_id=usuario_id,
        fecha=fecha_hoy,
        entrada=hora_actual,
        latitud=latitud,
        longitud=longitud,
        direccion=direccion
    )


    # =====================================================
    # GUARDAR
    # =====================================================

    db.session.add(jornada)
    db.session.commit()


    return jornada




def registrar_salida(usuario_id, zona_horaria="UTC"):

    jornada = obtener_jornada_abierta(
        usuario_id
    )

    if jornada is None:
        return None

    jornada.salida = obtener_hora_actual(
        zona_horaria
    )

    db.session.commit()

    return jornada
