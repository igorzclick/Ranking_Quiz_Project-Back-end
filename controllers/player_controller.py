from models.db import db
from models.player import Player
from flask import  request, redirect, url_for
from models.db import db

class PlayerController:
    @staticmethod
    def login():
        if request.method == "POST":
            name = request.form.get("name")
            if name:
                new_player = Player(name=name)
                db.session.add(new_player)
                db.session.commit()
                return redirect(url_for("start_game"))
        return '''
            <form method="post">
                Name: <input type="text" name="name">
                <input type="submit" value="Login">
            </form>
        '''
    @staticmethod
    def get_player(player_id):
        return Player.query.get(player_id)
    
    @staticmethod   
    def update_score(player_id, score):
        player = Player.query.get(player_id)
        if player:
            player.score = score
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_all_players():
        return Player.query.all()
    

    @staticmethod
    def delete_player(player_id):
        player = Player.query.get(player_id)
        if player:
            db.session.delete(player)
            db.session.commit()
            return True
        return False
    


    
