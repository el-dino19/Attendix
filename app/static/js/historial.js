setInterval(async function () {
    try {
        const response = await fetch("{{ url_for('auth.check_session') }}", {
            method: "GET",
            credentials: "same-origin",
            cache: "no-store",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        const data = await response.json();

        console.log("Estado de sesión:", data);

        // ==========================================
        // CUENTA DESACTIVADA (activo = 0)
        // ==========================================
        if (data.motivo === "cuenta_desactivada") {

            // Evitar que el modal aparezca varias veces
            if (document.getElementById("session-disabled-modal")) {
                return;
            }

            const modal = document.createElement("div");
            modal.id = "session-disabled-modal";

            modal.innerHTML = `
                <div style="
                    position: fixed;
                    inset: 0;
                    background: rgba(15, 23, 42, .65);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 99999;
                ">
                    <div style="
                        background: white;
                        width: min(420px, 90%);
                        border-radius: 20px;
                        padding: 32px;
                        text-align: center;
                        box-shadow: 0 20px 50px rgba(0,0,0,.2);
                    ">

                        <div style="
                            width: 65px;
                            height: 65px;
                            margin: 0 auto 20px;
                            border-radius: 50%;
                            background: #fee2e2;
                            color: #dc2626;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 28px;
                        ">
                            <i class="bi bi-person-x-fill"></i>
                        </div>

                        <h3 style="
                            margin-bottom: 10px;
                            color: #1e293b;
                        ">
                            Cuenta desactivada
                        </h3>

                        <p style="
                            color: #64748b;
                            margin-bottom: 25px;
                        ">
                            Tu cuenta ha sido desactivada por un administrador.
                            Tu sesión se cerrará.
                        </p>

                        <button
                            onclick="window.location.href='{{ url_for('auth.login') }}'"
                            style="
                                border: 0;
                                background: #dc2626;
                                color: white;
                                padding: 11px 25px;
                                border-radius: 10px;
                                font-weight: 600;
                                cursor: pointer;
                            "
                        >
                            Ir al inicio de sesión
                        </button>

                    </div>
                </div>
            `;

            document.body.appendChild(modal);
        }

        // ==========================================
        // SESIÓN EXPIRADA
        // ==========================================
        else if (data.motivo === "sesion_expirada") {

            window.location.href = "{{ url_for('auth.login') }}";
        }

        // ==========================================
        // USUARIO ELIMINADO
        // ==========================================
        else if (data.motivo === "usuario_no_existe") {

            window.location.href = "{{ url_for('auth.login') }}";
        }

        // ==========================================
        // USUARIO ACTIVO
        // activo = 1
        // ==========================================
        else if (
            data.activo === true &&
            data.sesion === true
        ) {

            // Todo correcto.
            // No hacemos nada.
        }

    } catch (error) {

        console.error(
            "Error comprobando la sesión:",
            error
        );
    }

}, 5000);
