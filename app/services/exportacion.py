from io import BytesIO
from datetime import date, timedelta

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def restar_meses(fecha, meses):
    """
    Resta meses a una fecha sin utilizar librerías externas.
    """
    año = fecha.year
    mes = fecha.month - meses

    while mes <= 0:
        mes += 12
        año -= 1

    return date(año, mes, 1)


def generar_excel_asistencia(
    registros,
    periodo="todos",
    mes=None
):
    """
    Genera el Excel de asistencia.

    Incluye:

    - Jornada
    - Entrada
    - Ubicación de inicio de jornada
    - Break mañana
    - Lunch
    - Break tarde
    - Salida
    - Inicio hora extra
    - Fin hora extra
    - Estado hora extra
    - Ubicación de inicio de hora extra

    periodo:

        "mes"
            Mes específico.
            Requiere mes="YYYY-MM"

        "3_meses"
            Mes actual + 2 meses anteriores.

        "6_meses"
            Mes actual + 5 meses anteriores.

        "todos"
            Todos los registros.

    mes:

        Formato YYYY-MM.
    """

    # ==========================================
    # CREAR LIBRO
    # ==========================================

    libro = Workbook()

    hoja = libro.active

    hoja.title = "Asistencia"

    # ==========================================
    # FECHA ACTUAL
    # ==========================================

    hoy = date.today()

    # ==========================================
    # RANGO DE FECHAS
    # ==========================================

    fecha_inicio = None
    fecha_fin = None

    # ==========================================
    # MES ESPECÍFICO
    # ==========================================

    if periodo == "mes":

        if not mes:
            raise ValueError(
                "Debes seleccionar un mes."
            )

        try:
            partes = mes.split("-")

            if len(partes) != 2:
                raise ValueError

            año = int(partes[0])
            numero_mes = int(partes[1])

            if numero_mes < 1 or numero_mes > 12:
                raise ValueError

            fecha_inicio = date(
                año,
                numero_mes,
                1
            )

            if numero_mes == 12:

                siguiente_mes = date(
                    año + 1,
                    1,
                    1
                )

            else:

                siguiente_mes = date(
                    año,
                    numero_mes + 1,
                    1
                )

            fecha_fin = (
                siguiente_mes
                - timedelta(days=1)
            )

        except (ValueError, TypeError):

            raise ValueError(
                "El mes debe tener el formato YYYY-MM."
            )

    # ==========================================
    # ÚLTIMOS 3 MESES
    # ==========================================

    elif periodo == "3_meses":

        fecha_inicio = restar_meses(
            hoy,
            2
        )

        fecha_fin = hoy

    # ==========================================
    # ÚLTIMOS 6 MESES
    # ==========================================

    elif periodo == "6_meses":

        fecha_inicio = restar_meses(
            hoy,
            5
        )

        fecha_fin = hoy

    # ==========================================
    # TODOS
    # ==========================================

    elif periodo == "todos":

        fecha_inicio = None
        fecha_fin = None

    else:

        raise ValueError(
            "Periodo inválido."
        )

    # ==========================================
    # ENCABEZADOS
    # ==========================================

    encabezados = [
        "ID Jornada",
        "Colaborador",
        "Correo",
        "Fecha",
        "Entrada",
        "Ubicación inicio jornada",
        "Break mañana",
        "Lunch",
        "Break tarde",
        "Salida",
        "Inicio hora extra",
        "Fin hora extra",
        "Estado hora extra",
        "Ubicación inicio hora extra"
    ]

    hoja.append(encabezados)

    # ==========================================
    # ESTILO ENCABEZADOS
    # ==========================================

    color_azul = "0D6EFD"

    fondo = PatternFill(
        fill_type="solid",
        fgColor=color_azul
    )

    borde = Border(
        bottom=Side(
            style="thin",
            color="FFFFFF"
        )
    )

    for celda in hoja[1]:

        celda.font = Font(
            bold=True,
            color="FFFFFF"
        )

        celda.fill = fondo

        celda.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

        celda.border = borde

    # ==========================================
    # FORMATO HORA 12 HORAS
    # ==========================================

    def formato_hora(hora):

        if hora is None:
            return ""

        return hora.strftime(
            "%I:%M:%S %p"
        )

    # ==========================================
    # FORMATO DESCANSO
    # ==========================================

    def formato_descanso(descanso):

        if descanso is None:
            return ""

        inicio = formato_hora(
            descanso.inicio
        )

        if descanso.fin:

            fin = formato_hora(
                descanso.fin
            )

        else:

            fin = "En curso"

        return f"{inicio} - {fin}"

    # ==========================================
    # RECORRER JORNADAS
    # ==========================================

    for jornada in registros:

        usuario = jornada.usuario

        # --------------------------------------
        # USUARIO NO EXISTE
        # --------------------------------------

        if usuario is None:
            continue

        # --------------------------------------
        # NO EXPORTAR ADMIN
        # --------------------------------------

        if (
            str(usuario.rol)
            .strip()
            .lower()
            == "admin"
        ):
            continue

        # ======================================
        # FILTRO POR FECHA
        # ======================================

        if periodo != "todos":

            if not jornada.fecha:
                continue

            fecha_jornada = jornada.fecha

            if hasattr(
                fecha_jornada,
                "date"
            ):

                fecha_jornada = (
                    fecha_jornada.date()
                )

            if (
                fecha_jornada < fecha_inicio
                or fecha_jornada > fecha_fin
            ):
                continue

        # ======================================
        # DESCANSOS
        # ======================================

        break_manana = None
        lunch = None
        break_tarde = None

        for descanso in jornada.descansos:

            if (
                descanso.tipo
                == "break_manana"
            ):

                break_manana = descanso

            elif (
                descanso.tipo
                == "lunch"
            ):

                lunch = descanso

            elif (
                descanso.tipo
                == "break_tarde"
            ):

                break_tarde = descanso

        # ======================================
        # HORA EXTRA
        # ======================================

        hora_extra = None

        if hasattr(
            jornada,
            "horas_extras"
        ):

            horas_extras = (
                jornada.horas_extras
            )

            if horas_extras:

                hora_extra = max(
                    horas_extras,
                    key=lambda h: (
                        h.inicio
                        if h.inicio
                        else ""
                    )
                )

        # ======================================
        # DATOS HORA EXTRA
        # ======================================

        if hora_extra:

            inicio_hora_extra = formato_hora(
                hora_extra.inicio
            )

            fin_hora_extra = formato_hora(
                hora_extra.fin
            )

            if hora_extra.fin:

                estado_hora_extra = (
                    "Completada"
                )

            else:

                estado_hora_extra = (
                    "En curso"
                )

            ubicacion_hora_extra = (
                hora_extra.direccion
                or ""
            )

        else:

            inicio_hora_extra = ""
            fin_hora_extra = ""
            estado_hora_extra = ""
            ubicacion_hora_extra = ""

        # ======================================
        # UBICACIÓN DE INICIO DE JORNADA
        # ======================================

        ubicacion_jornada = (
            jornada.direccion
            or ""
        )

        # ======================================
        # AGREGAR FILA
        # ======================================

        hoja.append([

            jornada.id,

            usuario.nombre,

            usuario.correo,

            jornada.fecha.strftime(
                "%Y-%m-%d"
            )
            if jornada.fecha
            else "",

            formato_hora(
                jornada.entrada
            ),

            ubicacion_jornada,

            formato_descanso(
                break_manana
            ),

            formato_descanso(
                lunch
            ),

            formato_descanso(
                break_tarde
            ),

            formato_hora(
                jornada.salida
            ),

            inicio_hora_extra,

            fin_hora_extra,

            estado_hora_extra,

            ubicacion_hora_extra

        ])

    # ==========================================
    # AJUSTAR COLUMNAS
    # ==========================================

    anchos = {

        1: 14,   # ID Jornada
        2: 25,   # Colaborador
        3: 35,   # Correo
        4: 15,   # Fecha
        5: 18,   # Entrada
        6: 45,   # Ubicación jornada
        7: 22,   # Break mañana
        8: 22,   # Lunch
        9: 22,   # Break tarde
        10: 18,  # Salida
        11: 22,  # Inicio hora extra
        12: 22,  # Fin hora extra
        13: 20,  # Estado hora extra
        14: 45   # Ubicación hora extra

    }

    for numero_columna, ancho in anchos.items():

        letra = get_column_letter(
            numero_columna
        )

        hoja.column_dimensions[
            letra
        ].width = ancho

    # ==========================================
    # CENTRAR COLUMNAS
    # ==========================================

    columnas_centradas = [

        0,   # ID
        3,   # Fecha
        4,   # Entrada
        6,   # Break mañana
        7,   # Lunch
        8,   # Break tarde
        9,   # Salida
        10,  # Inicio extra
        11,  # Fin extra
        12   # Estado extra

    ]

    for fila in hoja.iter_rows(
        min_row=2
    ):

        for indice in columnas_centradas:

            fila[indice].alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

    # ==========================================
    # TEXTO DE UBICACIONES
    # ==========================================

    for fila in hoja.iter_rows(
        min_row=2
    ):

        # Ubicación jornada
        fila[5].alignment = Alignment(
            horizontal="left",
            vertical="top",
            wrap_text=True
        )

        # Ubicación hora extra
        fila[13].alignment = Alignment(
            horizontal="left",
            vertical="top",
            wrap_text=True
        )

    # ==========================================
    # CONGELAR ENCABEZADO
    # ==========================================

    hoja.freeze_panes = "A2"

    # ==========================================
    # FILTRO EXCEL
    # ==========================================

    hoja.auto_filter.ref = hoja.dimensions

    # ==========================================
    # ALTURA ENCABEZADO
    # ==========================================

    hoja.row_dimensions[1].height = 35

    # ==========================================
    # CREAR ARCHIVO
    # ==========================================

    archivo = BytesIO()

    libro.save(
        archivo
    )

    archivo.seek(0)

    return archivo
