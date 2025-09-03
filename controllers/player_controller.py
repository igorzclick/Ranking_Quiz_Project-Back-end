from flask import render_template, request, redirect, url_for, session
from models.db import db
from models.player import Player

def login():
    if request.method == "POST":
        username = request.form["username"]
        player = Player.query.filter_by(username=username).first()
        if not player:
            player = Player(username)
            db.session.add(player)
            db.session.commit()
        session["player_id"] = player.id
        return redirect(url_for("home"))
    return render_template("login.html")