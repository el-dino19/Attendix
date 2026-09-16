from app import create_app
from app.services.recordatorio import revisar_jornadas


app = create_app()


with app.app_context():
    revisar_jornadas()
