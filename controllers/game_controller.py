from flask import render_template, request, redirect, url_for
from models.db import db
from models.game import Game
from models.questions import Question

def home():
    games = Game.query.all()
    return render_template("home.html", games=games)

def start_game():
    if request.method == "POST":
        secret_word = request.form["secret_word"]
        game = Game(secret_word)
        db.session.add(game)
        db.session.commit()
        return redirect(url_for("game_play", game_id=game.id))
    return render_template("game.html")

def game_play(game_id):
    game = Game.query.get_or_404(game_id)
    questions = Question.query.filter_by(game_id=game_id).all()
    return render_template("game.html", game=game, questions=questions)