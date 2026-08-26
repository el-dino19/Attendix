import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SQLALCHEMY_DATABASE_URI = os.getenv = (
        "mysql://avnadmin:AVNS_NrYJtDmKn5ZuNZN_vZp@asistencia-jeinerramirez1910-5925.k.aivencloud.com:20970/defaultdb?ssl_mode=REQUIRED"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = ("UcHvyj7At9KlYjDsJVlyV3LXmZ1pEDO03WpDyNwFCC9Li2mBVGpWvss3Bu7_3OEKbrZCH7MyxttWHZHNzE2Yzg")