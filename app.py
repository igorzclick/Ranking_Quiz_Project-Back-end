from flask import Flask, render_template, session
from config import Config
from models.db import db
from controllers import player_controller, game_controller, question_controller, guess_controller
from models.player import Player

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Rotas
app.add_url_rule("/", "home", game_controller.home)
app.add_url_rule("/login", "login", player_controller.login, methods=["GET", "POST"])
app.add_url_rule("/start", "start_game", game_controller.start_game, methods=["GET", "POST"])
app.add_url_rule("/game/<int:game_id>", "game_play", game_controller.game_play)
app.add_url_rule("/game/<int:game_id>/question", "add_question", question_controller.add_question, methods=["POST"])
app.add_url_rule("/game/<int:game_id>/guess", "make_guess", guess_controller.make_guess, methods=["POST"])
    
@app.route("/result/<int:game_id>/<int:player_id>")
def result(game_id, player_id): 
    from models.game import Game
    from models.player import player
    game = Game.query.get_or_404(game_id)
    player = Player.query.get_or_404(player_id)
    return render_template("result.html", game=game, player=player)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
