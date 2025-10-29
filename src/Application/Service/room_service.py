from src.Infrastructure.Model.room_model import Room
from src.Infrastructure.Model.player_model import Player
from src.Infrastructure.Model.theme_model import Theme
from src.config.data_base import db


class RoomService:
    @staticmethod
    def create_room(room_domain):
        new_room = room_domain.to_dict()
        try:
            player = Player.query.filter_by(id=new_room['created_by']).first()
            if not player:
                return None, "Player not found"

            theme = Theme.query.filter_by(id=new_room['theme_id']).first()
            if not theme:
                return None, "Theme not found"

            room = Room(**new_room)
            db.session.add(room)
            db.session.commit()

            return room, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_room_by_id(room_id):
        try:
            room = Room.query.filter_by(id=room_id).first()
            if not room:
                return None, "Room not found"
            return room.to_dict(), None
        except Exception as e:
            return None, str(e)


