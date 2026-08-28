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

        try:

            correo = request.form.get(
                "correo",
                ""
            ).strip()

            password = request.form.get(
                "password",
                ""
            )

            print("DEBUG 1 - Login recibido")
            print("DEBUG 2 - Correo:", correo)

            if not correo or not password:

                flash(
                    "Debes ingresar correo y contraseña.",
                    "error"
                )

                return render_template("login.html")

            print("DEBUG 3 - Intentando autenticar")

            usuario = autenticar_usuario(
                correo,
                password
            )

            print("DEBUG 4 - Usuario:", usuario)

            if usuario is None:

                flash(
                    "Correo o contraseña incorrectos.",
                    "error"
                )

                return render_template("login.html")

            print("DEBUG 5 - Usuario encontrado")
            print("DEBUG 6 - ID:", usuario.id)
            print("DEBUG 7 - Rol:", usuario.rol)

            session.clear()

            session["usuario_id"] = usuario.id
            session["nombre"] = usuario.nombre
            session["correo"] = usuario.correo
            session["rol"] = usuario.rol

            print("DEBUG 8 - Sesión creada")

            # TEMPORALMENTE DESACTIVADO
            # registrar_entrada(usuario.id)

            print("DEBUG 9 - Antes de redireccionar")

            if usuario.rol == "admin":

                return redirect(
                    url_for("admin.dashboard")
                )

            return redirect(
                url_for("empleado.dashboard")
            )

        except Exception as e:

            print("====================================")
            print("ERROR REAL DEL LOGIN:")
            print(type(e).__name__)
            print(str(e))
            print("====================================")

            raise

    return render_template(
        "login.html"
    )



@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )