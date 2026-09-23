# Attendix — ampliación multi-grupo

## Arquitectura

- `admin_global`: controla toda la plataforma.
- `Grupo`: unidad independiente de asistencia.
- `GrupoMiembro`: relación entre usuarios y grupos.
- `GrupoMiembro.rol = admin`: administrador de ese grupo.
- `GrupoMiembro.rol = colaborador`: empleado/colaborador del grupo.
- `Jornada.grupo_id`: identifica a qué grupo pertenece la asistencia.
- `HoraExtra.grupo_id`: identifica a qué grupo pertenece la hora extra.

Esto evita usar un único `rol="admin"` para representar permisos de toda la plataforma.

## Flujo

1. Administrador global inicia sesión.
2. Crea grupos.
3. Crea usuarios colaboradores.
4. Asigna usuarios a grupos como `admin` o `colaborador`.
5. El administrador de grupo solo gestiona su grupo.
6. El colaborador registra asistencia dentro de su grupo.
7. Los historiales y horas extra se filtran por grupo.
8. Si un colaborador pertenece a varios grupos, selecciona el grupo al iniciar sesión.

## Archivos modificados

- `app/models/usuario.py`
- `app/models/jornada.py`
- `app/models/hora_extra.py`
- `app/models/__init__.py`
- `app/services/asistencia.py`
- `app/services/horas_extras.py`
- `app/services/historial.py`
- `app/services/usuarios_admin.py`
- `app/routes/auth.py`
- `app/routes/empleado.py`
- `app/routes/admin.py`

## Archivos nuevos

- `app/models/grupo.py`
- `app/models/grupo_miembro.py`
- `app/services/grupos.py`
- `app/routes/grupos.py`
- `migrations/migrar_multigrupo.py`

## Nota

Las rutas originales `admin.py`, `auth.py` y `empleado.py` están en los archivos que enviaste. En este paquete se han colocado en `app/routes/` para dejar explícita una estructura de proyecto. Si en tu proyecto real están en otra carpeta, reemplaza los archivos equivalentes sin mover carpetas.

El servicio de descansos también fue actualizado para recibir `grupo_id`, de forma que una jornada de otro grupo no pueda ser tomada como jornada activa por accidente.
