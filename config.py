import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "segredo")
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "senha"
    MYSQL_DB = "perfil_db"