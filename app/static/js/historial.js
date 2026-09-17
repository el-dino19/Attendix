 let cuentaDesactivada = false;

    async function verificarEstadoCuenta() {

        if (cuentaDesactivada) {
            return;
        }

        try {

            const response = await fetch(
                "{{ url_for('auth.verificar_estado') }}",
                {
                    method: "GET",
                    credentials: "same-origin",
                    cache: "no-store"
                }
            );

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            if (data.activo === false) {

                cuentaDesactivada = true;

                const modalElement =
                    document.getElementById(
                        "modalCuentaDesactivada"
                    );

                const modal =
                    new bootstrap.Modal(
                        modalElement,
                        {
                            backdrop: "static",
                            keyboard: false
                        }
                    );

                modal.show();

                // Cerrar sesión después de 3 segundos
                setTimeout(function () {

                    window.location.href =
                        "{{ url_for('auth.logout') }}";

                }, 3000);
            }

        } catch (error) {

            console.error(
                "Error verificando cuenta:",
                error
            );

        }
    }


    // Revisar cada 5 segundos
    setInterval(
        verificarEstadoCuenta,
        5000
    );


    // Revisar inmediatamente al cargar la página
    verificarEstadoCuenta();


    // Si pulsa Aceptar
    document
        .getElementById("btnCuentaDesactivada")
        .addEventListener("click", function () {

            window.location.href =
                "{{ url_for('auth.logout') }}";

        });