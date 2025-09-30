from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from src.Application.Service.theme_service import ThemeService
from src.Domain.theme import ThemeDomain

THEME_NOT_FOUND = "Theme not found"

class ThemeController:
    @staticmethod
    def register_theme(body):
        player_id = get_jwt_identity()
        
        theme_domain = ThemeDomain(
            name=body['name'],
            description=body['description'],
            is_active=True,  
            created_by=player_id
        )
        theme, error_message = ThemeService.create_theme(theme_domain)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)

        return make_response(jsonify({
            "message": "Theme registered successfully",
            "theme": theme.to_dict()
        }), 201)

    @staticmethod
    def get_all_themes():
        themes = ThemeService.get_all_themes()
        if themes is None:
            return make_response(jsonify({"message": "Could not retrieve themes"}), 500)
        return make_response(jsonify({"themes": themes}), 200)

    @staticmethod
    def get_theme_by_id(theme_id):
        theme = ThemeService.get_theme_by_id(theme_id)
        if not theme:
             return make_response(jsonify({"message": THEME_NOT_FOUND}), 404)
        return make_response(jsonify({
            "theme": theme
        }), 200)

    @staticmethod
    def get_theme_by_name(theme_name):
        theme = ThemeService.get_theme_by_name(theme_name)
        if not theme:
             return make_response(jsonify({"message": THEME_NOT_FOUND}), 404)
        return make_response(jsonify({
            "theme": theme
        }), 200)

    @staticmethod
    def update_theme(body):
        theme_domain = ThemeDomain(
            name=body['name'],
            description=body['description'],
            is_active=body.get('is_active', True),
            created_by=body.get('created_by')
        )
        theme, error_message = ThemeService.update_theme(theme_domain)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not theme:
            return make_response(jsonify({"message": f"{THEME_NOT_FOUND} or update failed"}), 404)

        return make_response(jsonify({
            "message": "Theme updated successfully",
            "theme": theme.to_dict()
        }), 200)
    
    @staticmethod
    def delete_theme(theme_id):
        theme = ThemeService.delete_theme(theme_id)
        if not theme:
            return make_response(jsonify({"message": THEME_NOT_FOUND}), 404)

        return make_response(jsonify({
            "message": "Theme deleted successfully",
        }), 200)