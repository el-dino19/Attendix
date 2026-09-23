"""
Migración de Attendix a arquitectura multi-grupo.

Ejecutar dentro del contexto de la aplicación, por ejemplo:
    flask shell
    >>> exec(open("migrations/migrar_multigrupo.py", encoding="utf-8").read())

El script:
1. crea grupos y grupo_miembros;
2. agrega grupo_id a jornadas y horas_extras si falta;
3. convierte el antiguo rol "admin" en "admin_global";
4. crea un "Grupo General" y asigna allí a los empleados existentes;
5. relaciona jornadas/horas extra antiguas con el Grupo General.

IMPORTANTE: haz una copia de seguridad de la BD antes de ejecutarlo.
"""

from sqlalchemy import inspect, text
from app import db
from app.models import Usuario, Grupo, GrupoMiembro


def agregar_columna_si_falta(tabla, columna, definicion):
    inspector = inspect(db.engine)
    columnas = {c["name"] for c in inspector.get_columns(tabla)}
    if columna not in columnas:
        with db.engine.begin() as conn:
            conn.execute(text(
                f'ALTER TABLE {tabla} ADD COLUMN {columna} {definicion}'
            ))


def ejecutar():
    # Las tablas nuevas se crean mediante los modelos.
    db.create_all()

    # Compatibilidad con el rol anterior.
    Usuario.query.filter(Usuario.rol == "admin").update(
        {Usuario.rol: "admin_global"},
        synchronize_session=False
    )

    # Las columnas nuevas se agregan si la BD existente todavía no las tiene.
    agregar_columna_si_falta("jornadas", "grupo_id", "INTEGER")
    agregar_columna_si_falta("horas_extras", "grupo_id", "INTEGER")

    grupo = Grupo.query.filter_by(nombre="Grupo General").first()

    if grupo is None:
        global_admin = (
            Usuario.query
            .filter(Usuario.rol == "admin_global")
            .order_by(Usuario.id.asc())
            .first()
        )
        grupo = Grupo(
            nombre="Grupo General",
            descripcion="Grupo creado durante la migración de Attendix.",
            creado_por=global_admin.id if global_admin else None,
            activo=True
        )
        db.session.add(grupo)
        db.session.flush()

    empleados = Usuario.query.filter(
        Usuario.rol == "empleado"
    ).all()

    for usuario in empleados:
        membresia = GrupoMiembro.query.filter_by(
            grupo_id=grupo.id,
            usuario_id=usuario.id
        ).first()

        if membresia is None:
            db.session.add(
                GrupoMiembro(
                    grupo_id=grupo.id,
                    usuario_id=usuario.id,
                    rol="colaborador",
                    activo=True
                )
            )

    # Asignar registros históricos al Grupo General solo cuando no tengan grupo.
    db.session.flush()
    with db.engine.begin() as conn:
        conn.execute(
            text("UPDATE jornadas SET grupo_id = :gid WHERE grupo_id IS NULL"),
            {"gid": grupo.id}
        )
        conn.execute(
            text("UPDATE horas_extras SET grupo_id = :gid WHERE grupo_id IS NULL"),
            {"gid": grupo.id}
        )

    db.session.commit()
    print("Migración multi-grupo completada.")
    print("Grupo creado/recuperado:", grupo.id, grupo.nombre)


if __name__ == "__main__":
    ejecutar()
