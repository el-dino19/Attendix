from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

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
                "error"
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
                "error"
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