import os
from datetime import timedelta

class JWTConfig:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ranking-quiz-super-secret-jwt-key-2024")
    ACCESS_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 1))
    )
    REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 7))
    )