from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)
from app.models import Usuario

from app.services.autenticacion import autenticar_usuario
from app.services.asistencia import registrar_entrada


auth_bp = Blueprint(
    "auth",
    __name__
)



@auth_bp.route("/")
def inicio():
    return render_template(
                    "login.html"
                )

@auth_bp.route("/health")
def health():
    return "OK", 200

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # ========================================
    # PETICIÓN POST
    # ========================================

    if request.method == "POST":

        # ========================================
        # DATOS DEL FORMULARIO
        # ========================================

        correo = request.form.get(
            "correo",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # ========================================
        # ZONA HORARIA DEL NAVEGADOR
        # ========================================

        zona_horaria = request.form.get(
            "zona_horaria",
            "UTC"
        ).strip()

        # ========================================
        # UBICACIÓN DEL NAVEGADOR
        # ========================================

        latitud = request.form.get(
            "latitud"
        )

        longitud = request.form.get(
            "longitud"
        )

        direccion = request.form.get(
            "direccion",
            ""
        ).strip()

        # ========================================
        # CONVERTIR COORDENADAS
        # ========================================

        try:

            latitud = (
                float(latitud)
                if latitud
                else None
            )

            longitud = (
                float(longitud)
                if longitud
                else None
            )

        except (ValueError, TypeError):

            latitud = None
            longitud = None

        # ========================================
        # VALIDAR CAMPOS
        # ========================================

        if not correo or not password:

            flash(
                "Debes ingresar correo y contraseña.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        # ========================================
        # AUTENTICAR USUARIO
        # ========================================

        usuario = autenticar_usuario(
            correo,
            password
        )

        # ========================================
        # USUARIO NO EXISTE /
        # CONTRASEÑA INCORRECTA
        # ========================================

        if usuario is None:

            flash(
                "Correo o contraseña incorrectos.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        # ========================================
        # VALIDAR ESTADO
        # ========================================

        if not usuario.activo:

            flash(
                "Tu cuenta está desactivada. "
                "Contacta con un administrador para recuperar el acceso.",
                "warning"
            )

            return render_template(
                "login.html"
            )

        # ========================================
        # CREAR SESIÓN
        # ========================================

        session.clear()

        session["usuario_id"] = usuario.id
        session["nombre"] = usuario.nombre
        session["correo"] = usuario.correo
        session["rol"] = usuario.rol

        # Guardar zona horaria para utilizarla
        # también al registrar la salida.

        session["zona_horaria"] = zona_horaria

        # ========================================
        # REGISTRAR ENTRADA
        # ========================================

        if usuario.rol == "empleado":

            registrar_entrada(
                usuario.id,
                zona_horaria,
                latitud,
                longitud,
                direccion
            )

        # ========================================
        # REDIRECCIÓN SEGÚN ROL
        # ========================================

        if usuario.rol == "admin":

            return redirect(
                url_for("admin.dashboard")
            )

        return redirect(
            url_for("empleado.dashboard")
        )

    # ========================================
    # PETICIÓN GET
    # ========================================

    return render_template(
        "login.html"
    )


#===========================
# CERRAR SESION
# ==========================

@auth_bp.route("/logout")
def logout():
    

    session.clear()

    return redirect(
        url_for("auth.login")
    )
    

#===========================
# VERIFICAR ESTADO
# ==========================
@auth_bp.route("/verificar-estado")
def verificar_estado():

    usuario_id = session.get("usuario_id")

    # No hay sesión activa
    if not usuario_id:
        return jsonify({
            "autenticado": False
        }), 401

    usuario = Usuario.query.get(usuario_id)

    # Usuario eliminado
    if usuario is None:
        session.clear()

        return jsonify({
            "autenticado": False,
            "activo": False
        }), 401

    # Usuario desactivado
    if not usuario.activo:
        session.clear()

        return jsonify({
            "autenticado": True,
            "activo": False
        }), 200

    return jsonify({
        "autenticado": True,
        "activo": True
    }), 200
