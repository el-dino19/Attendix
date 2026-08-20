from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)

bcrypt = Bcrypt(app)


password = input("Escribe la contraseña: ")

password_hash = bcrypt.generate_password_hash(
    password
).decode("utf-8")

print()
print("HASH:")
print(password_hash)