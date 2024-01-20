from app import jwt
from app.auth import bp
from app.auth.helpers import get_users, get_user, add_user, remove_user, encrypt_pwd, check_pwd
from app.auth.models import Users, InvalidToken
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, \
    jwt_required
# from config import Config

@jwt.token_in_blocklist_loader
def check_if_blacklisted_token(data, decrypted):
    """
    Decorator designed to check for blacklisted tokens
    """
    jti = decrypted['jti']
    return InvalidToken.is_invalid(jti)


@bp.route("/login", methods=["POST"])
def login():
    """
    User login end-point accepts email and password.
    returns jwt_token
    """
    try:
        username = request.json["username"]
        pwd = request.json["pwd"]
        if username and pwd:
            user = list(filter(lambda x: x["username"] == username and check_pwd(pwd, x["pwd"]), get_users()))
            if len(user) == 1:
                token = create_access_token(identity=user[0]["id"])
                refresh_token = create_refresh_token(identity=user[0]["id"])
                user[0]["token"] = token
                return jsonify({"token": token, "refreshToken": refresh_token, "user": user[0]}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401
        else:           
            return jsonify({"error":"Invalid Form"}), 400
    except:
        return jsonify({"error": "Invalid Form"}), 500


@bp.route("/register", methods=["POST"])
def register():
    """
    End-point to handle user registration, encrypting the password and validating the email
    """
    try:
        
        pwd = encrypt_pwd(request.json['pwd'])
        username = request.json['username']
        email = request.json['email']
        
        users = get_users()

        if len(list(filter(lambda x: x["username"] == username, users))) == 1:         
            return jsonify({"error": "Invalid Form"})
        
        add_user(email=email, username=username, pwd=pwd)
        
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/checkiftokenexpire", methods=["POST"])
@jwt_required()
def check_if_token_expire():
    """
    End-point for frontend to check if the token has expired or not
    """
    return jsonify({"success": True}), 200


@bp.route("/refreshtoken", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    End-point to refresh the token when required
    
    """
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)
    return jsonify({"token": token}), 200


@bp.route("/getcurrentuser")
@jwt_required()
def current_user():
    """
    End-point to handle collecting the current user information
    """
    uid = get_jwt_identity()
    return jsonify(get_user(uid)), 200


@bp.route("/logout/access", methods=["POST"])
@jwt_required()
def access_logout():
    """
    End-point to log the user out and Invalidate the token.
    """
    jti = get_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success":True}), 200
    except Exception as e:
        print("error occured")
        print(e)
        return jsonify({"error": str(e)}), 500


@bp.route("/logout/refresh", methods=["POST"])
@jwt_required()
def refresh_logout():
    """
    End-point to invalidate the token.
    Can be used with both log the user out or for the frontend to call after refreshing the token.

    """
    
    jti = get_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@bp.route("/deleteaccount", methods=["DELETE"])
@jwt_required()
def delete_account():
    """
    End-point to handle removal of users
    """
    try:
        user = get_user(get_jwt_identity())
        remove_user(user.id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500