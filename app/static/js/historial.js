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

            const data = await response.json();

            console.log("Estado de cuenta:", data);

            if (data.activo === false) {

                cuentaDesactivada = true;

                const modalElement =
                    document.getElementById(
                        "modalCuentaDesactivada"
                    );

                if (!modalElement) {
                    console.error(
                        "No se encontró la modal #modalCuentaDesactivada"
                    );
                    return;
                }

                const modal =
                    new bootstrap.Modal(
                        modalElement,
                        {
                            backdrop: "static",
                            keyboard: false
                        }
                    );

                modal.show();

                // Después de 3 segundos cerrar sesión
                setTimeout(function () {

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


    // Revisar inmediatamente
    verificarEstadoCuenta();


    // Botón aceptar
    const boton =
        document.getElementById(
            "btnCuentaDesactivada"
        );

    if (boton) {

        boton.addEventListener(
            "click",
            function () {

                window.location.href =
                    "{{ url_for('auth.logout') }}";

            }
        );
    }