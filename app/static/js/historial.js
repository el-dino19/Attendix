

let cuentaDesactivada = false;

async function verificarEstadoCuenta() {

    // Evitar hacer más peticiones después de detectar
    // que la cuenta fue desactivada.
    if (cuentaDesactivada) {
        return;
    }

    try {

        const respuesta = await fetch(
            "{{ url_for('auth.verificar_estado') }}",
            {
                method: "GET",
                credentials: "same-origin",
                cache: "no-store"
            }
        );

        const datos = await respuesta.json();

        // La cuenta fue desactivada
        if (datos.activo === false) {

            cuentaDesactivada = true;

            const modalElement = document.getElementById(
                "cuentaDesactivadaModal"
            );

            const modal = new bootstrap.Modal(
                modalElement,
                {
                    backdrop: "static",
                    keyboard: false
                }
            );

            modal.show();

            // Cerrar sesión automáticamente
            setTimeout(() => {

                window.location.href =
                    "{{ url_for('auth.logout') }}";

            }, 3000);
        }

    } catch (error) {

        console.error(
            "Error verificando estado de cuenta:",
            error
        );

    }
}


// Revisar cada 5 segundos
setInterval(
    verificarEstadoCuenta,
    5000
);


// Verificar también inmediatamente
verificarEstadoCuenta();


// Botón Aceptar
document
    .getElementById("btnCerrarCuentaDesactivada")
    .addEventListener("click", function () {

        window.location.href =
            "{{ url_for('auth.logout') }}";

    });


