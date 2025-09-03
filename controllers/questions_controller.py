from flask import request, redirect, url_for
from models.db import db
from models.questions import Question

def add_question(game_id):
    if request.method == "POST":
        text = request.form["question"]
        question = Question(text, game_id)
        db.session.add(question)
        db.session.commit()
    return redirect(url_for("game_play", game_id=game_id))