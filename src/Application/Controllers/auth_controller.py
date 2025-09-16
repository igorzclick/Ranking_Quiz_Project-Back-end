from flask import jsonify, make_response
from src.Domain.auth import AuthDomain
from src.Application.Service.auth_service import AuthService

class AuthController:
    @staticmethod
    def login(body):
        authDomain = AuthDomain(
            username=body['nickname'],
            password=body['password']
        ).to_dict()
        
        token, error, code = AuthService.login(authDomain)
        
        if(error):
            return make_response(jsonify({
            "message": error,
        }), code)

        return make_response(jsonify({
            "message": "Login successful",
            "access_token": token,
        }), code)