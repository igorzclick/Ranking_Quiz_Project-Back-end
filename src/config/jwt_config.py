import os
from datetime import timedelta



class JWTConfig:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
    ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 30))
    )
    REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 7))
    )