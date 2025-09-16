from apiflask import APIFlask
from src.config.data_base import init_db
from src.Application.Dto.player_dto import PlayerRegisterSchema
from src.Application.Service.player_service import PlayerService
from src.routes import init_routes
from src.config.jwt_config import JWTConfig
from flask_jwt_extended import JWTManager

def create_app():
    """
    Fun o que cria e configura a aplica o Flask.
    """
 
    app = APIFlask(__name__)
    # Configure Flask-JWT-Extended
    app.config["JWT_SECRET_KEY"] = "grupinho_2.0"
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    jwt = JWTManager(app)

    init_db(app)

    init_routes(app)

    return app

app = create_app()

if __name__ == '__name__':
    app.run(debug=True, host='0.0.0.0')