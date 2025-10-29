from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from src.Application.Service.room_service import RoomService
from src.Domain.room import RoomDomain


class RoomController:
    @staticmethod
    def create_room(body):
        player_id = get_jwt_identity()

        room_domain = RoomDomain(
            title=body['title'],
            theme_id=body['theme_id'],
            created_by=player_id,
        )

        room, error_message = RoomService.create_room(room_domain)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)

        return make_response(jsonify({
            "message": "Room created successfully",
            "room": room.to_dict()
        }), 201)

    @staticmethod
    def get_room_by_id(room_id):
        room, error_message = RoomService.get_room_by_id(room_id)
        if error_message:
            status = 404 if error_message == "Room not found" else 400
            return make_response(jsonify({"message": error_message}), status)
        return make_response(jsonify({"room": room}), 200)


