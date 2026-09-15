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

    if request.method == "POST":

        try:

            # ==========================================
            # DATOS DEL FORMULARIO
            # ==========================================

            correo = request.form.get(
                "correo",
                ""
            ).strip().lower()

            password = request.form.get(
                "password",
                ""
            )

            print("========================================")
            print("LOGIN")
            print("Correo recibido:", correo)
            print("========================================")


            # ==========================================
            # VALIDAR
            # ==========================================

            if not correo or not password:

                flash(
                    "Debes ingresar correo y contraseña.",
                    "danger"
                )

                return render_template(
                    "login.html"
                )


            # ==========================================
            # AUTENTICAR
            # ==========================================

            print("Intentando autenticar usuario...")

            usuario = autenticar_usuario(
                correo,
                password
            )

            print(
                "Resultado autenticación:",
                usuario
            )


            # ==========================================
            # USUARIO NO EXISTE
            # ==========================================

            if usuario is None:

                flash(
                    "Correo o contraseña incorrectos.",
                    "danger"
                )

                return render_template(
                    "login.html"
                )


            print(
                "Usuario encontrado:",
                usuario.id,
                usuario.nombre,
                usuario.rol
            )


            # ==========================================
            # VALIDAR ESTADO
            # ==========================================

            if not usuario.activo:

                flash(
                    "Tu cuenta está desactivada.",
                    "warning"
                )

                return render_template(
                    "login.html"
                )


            # ==========================================
            # CREAR SESIÓN
            # ==========================================

            print("Creando sesión...")

            session.clear()

            session["usuario_id"] = usuario.id
            session["nombre"] = usuario.nombre
            session["correo"] = usuario.correo
            session["rol"] = usuario.rol


            print(
                "Sesión creada:",
                dict(session)
            )


            # ==========================================
            # REGISTRAR ENTRADA
            # ==========================================

            print("Registrando entrada...")

            registrar_entrada(
                usuario.id
            )

            print("Entrada registrada correctamente.")


            # ==========================================
            # REDIRECCIÓN
            # ==========================================

            print(
                "Rol del usuario:",
                usuario.rol
            )


            if usuario.rol == "admin":

                print("Redirigiendo a admin...")

                return redirect(
                    url_for("admin.dashboard")
                )


            print("Redirigiendo a empleado...")

            return redirect(
                url_for("empleado.dashboard")
            )


        except Exception as e:

            # ==========================================
            # MOSTRAR ERROR REAL
            # ==========================================

            import traceback

            print("")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("ERROR DURANTE LOGIN")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(
                "TIPO:",
                type(e).__name__
            )
            print(
                "ERROR:",
                str(e)
            )
            print("TRACEBACK:")
            traceback.print_exc()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("")

            flash(
                "Ocurrió un error interno al iniciar sesión.",
                "danger"
            )

            return render_template(
                "login.html"
            )


@auth_bp.route("/logout")
def logout():
    

    session.clear()

    return redirect(
        url_for("auth.login")
    )
    


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
