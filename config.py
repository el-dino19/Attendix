import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # MYSQL_HOST = os.getenv("MYSQL_HOST")
    # MYSQL_USER = os.getenv("MYSQL_USER")
    # MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    # MYSQL_PORT = os.getenv("MYSQL_PORT")
    # MYSQL_DB = os.getenv("MYSQL_DB")
    # MYSQL_CHARSET = os.getenv("MYSQL_CHARSET")

    # MYSQL_URI = os.getenv("MYSQL_URI")

    SQLALCHEMY_DATABASE_URI = os.getenv = (
        "mysql://avnadmin:AVNS_NrYJtDmKn5ZuNZN_vZp@asistencia-jeinerramirez1910-5925.k.aivencloud.com:20970/defaultdb?ssl_mode=REQUIRED"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = ("UcHvyj7At9KlYjDsJVlyV3LXmZ1pEDO03WpDyNwFCC9Li2mBVGpWvss3Bu7_3OEKbrZCH7MyxttWHZHNzE2Yzg")