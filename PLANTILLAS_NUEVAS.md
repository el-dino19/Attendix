# Plantillas nuevas necesarias

La lógica Python ya queda preparada, pero tu interfaz actual necesita estas plantillas:

- `templates/grupos/seleccionar.html`
- `templates/grupos/dashboard.html`
- `templates/grupos/mis_grupos.html`
- `templates/admin/grupos.html`
- `templates/admin/grupo_miembros.html`

No he reemplazado tus plantillas existentes porque no fueron adjuntadas en este proyecto.

## Datos que deben mostrar

### grupos/seleccionar.html
Un botón por grupo:
- nombre
- descripción
- POST a `/Attendix/grupos/seleccionar/<grupo_id>`

### grupos/dashboard.html
Debe mostrar:
- nombre del grupo
- administradores y colaboradores
- formulario para agregar usuario
- rol: `admin` o `colaborador`
- opción para retirar miembro

### admin/grupos.html
Para el administrador global:
- crear grupo
- listar grupos
- entrar a gestionar miembros

### admin/grupo_miembros.html
Para el administrador global:
- seleccionar usuario
- seleccionar rol
- agregar al grupo

## Registro de blueprints

En tu `app` debes registrar:
- `auth_bp` desde `app.routes.auth`
- `admin_bp` desde `app.routes.admin`
- `empleado_bp` desde `app.routes.empleado`
- `grupos_bp` desde `app.routes.grupos`

Si tus archivos de rutas están directamente en otra carpeta, conserva tu estructura actual y copia únicamente las funciones equivalentes.
