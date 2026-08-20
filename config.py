class Config:
    SECRET_KEY = "12345678"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:@localhost/asistencia"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False