from apiflask import APIFlask
from src.config.data_base import init_db
from src.Application.Dto.player_dto import PlayerRegisterSchema
from src.Application.Service.player_service import PlayerService
from src.routes import init_routes
from src.config.jwt_config import JWTConfig
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS

# carregar o dotenv
load_dotenv()

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
 
    app = APIFlask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # configuração Flask-JWT-Extended
    app.config["JWT_SECRET_KEY"] = JWTConfig.SECRET_KEY
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWTConfig.ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = JWTConfig.REFRESH_TOKEN_EXPIRES
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    jwt = JWTManager(app)

    init_db(app)

    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')