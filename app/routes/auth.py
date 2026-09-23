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
from app.services.grupos import obtener_grupos_usuario, es_admin_grupo


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def inicio():
    return render_template("login.html")


@auth_bp.route("/health")
def health():
    return "OK", 200


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "")
        zona_horaria = request.form.get(
            "zona_horaria", "UTC"
        ).strip()

        latitud = request.form.get("latitud")
        longitud = request.form.get("longitud")
        direccion = request.form.get("direccion", "").strip()

        try:
            latitud = float(latitud) if latitud else None
            longitud = float(longitud) if longitud else None
        except (ValueError, TypeError):
            latitud = None
            longitud = None

        if not correo or not password:
            flash("Debes ingresar correo y contraseña.", "danger")
            return render_template("login.html")

        usuario = autenticar_usuario(correo, password)

        if usuario is None:
            flash("Correo o contraseña incorrectos.", "danger")
            return render_template("login.html")

        if not usuario.activo:
            flash(
                "Tu cuenta está desactivada. Contacta con un administrador para recuperar el acceso.",
                "warning"
            )
            return render_template("login.html")

        session.clear()
        session["usuario_id"] = usuario.id
        session["nombre"] = usuario.nombre
        session["correo"] = usuario.correo
        session["rol"] = usuario.rol
        session["zona_horaria"] = zona_horaria

        if usuario.rol == "admin_global":
            return redirect(url_for("admin.dashboard"))

        grupos = obtener_grupos_usuario(usuario.id)

        if not grupos:
            flash(
                "Tu usuario no tiene ningún grupo activo asignado. Contacta al administrador.",
                "warning"
            )
            return redirect(url_for("auth.logout"))

        # Guardamos la ubicación del login hasta seleccionar el grupo.
        session["login_latitud"] = latitud
        session["login_longitud"] = longitud
        session["login_direccion"] = direccion

        if len(grupos) == 1:
            grupo = grupos[0]
            session["grupo_id"] = grupo.id
            session["grupo_nombre"] = grupo.nombre

            if es_admin_grupo(grupo.id, usuario.id):
                return redirect(url_for("grupos.dashboard", grupo_id=grupo.id))

            registrar_entrada(
                usuario.id,
                zona_horaria,
                latitud,
                longitud,
                direccion,
                grupo.id
            )

            session.pop("login_latitud", None)
            session.pop("login_longitud", None)
            session.pop("login_direccion", None)

            return redirect(url_for("empleado.dashboard"))

        return redirect(url_for("grupos.seleccionar"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/verificar-estado")
def verificar_estado():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({
            "autenticado": False,
            "activo": False
        }), 401

    usuario = Usuario.query.get(usuario_id)

    if usuario is None:
        session.clear()
        return jsonify({
            "autenticado": False,
            "activo": False
        }), 401

    if not usuario.activo:
        session.clear()
        return jsonify({
            "autenticado": False,
            "activo": False
        }), 401

    return jsonify({
        "autenticado": True,
        "activo": True
    }), 200
