
setInterval(async function () {
    try {
        const response = await fetch("{{ url_for('auth.check_session') }}", {
            method: "GET",
            credentials: "same-origin",
            cache: "no-store",
        });

        if (!response.ok) {
            const modal = document.createElement("div");

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
    } catch (error) {
        console.error("Error comprobando la sesión:", error);
    }
}, 5000);
