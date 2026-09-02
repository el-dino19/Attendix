from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
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

    if request.method == "POST":

        correo = request.form.get(
            "correo",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

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

        if usuario is None:

            flash(
                "Correo o contraseña incorrectos.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        # ========================================
        # VALIDAR ESTADO DE LA CUENTA
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

        # ========================================
        # REGISTRAR ENTRADA
        # ========================================

        registrar_entrada(
            usuario.id
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

    # ============================================
    # PETICIÓN GET
    # ============================================

    return render_template(
        "login.html"
    )

@auth_bp.route("/logout")
def logout():
    

    session.clear()

    return redirect(
        url_for("auth.login")
    )
    
from flask import session, jsonify

@auth_bp.route("/check-session")
def check_session():

    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({
            "activo": False,
            "sesion": False
        }), 401

    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        session.clear()

        return jsonify({
            "activo": False,
            "sesion": False
        }), 401

    if not usuario.activo:
        session.clear()

        return jsonify({
            "activo": False,
            "sesion": False
        }), 401

    return jsonify({
        "activo": True,
        "sesion": True
    })
