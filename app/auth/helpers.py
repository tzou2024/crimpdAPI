from app import db
from app.auth.models import Users
from bcrypt import hashpw, gensalt, checkpw
from base64 import b64encode
from hashlib import sha256

def get_users():
    users = Users.query.all()
    
    return [{"id": i.id, "email": i.email, "username": i.username, "pwd": i.pwd, "role": i.role} for i in users]

def get_user(user_id):
    users = Users.query.all()
    user = list(filter(lambda x: x.id == user_id, users))[0]
    return {"id": user.id, "username": user.username, "email": user.email, "pwd": user.pwd, "role": user.role}

def add_user(email, username, pwd):
    if username and pwd and email:
        try:
            user = Users(email, username, pwd)
            user.save()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False
    
def remove_user(user_id):
    if user_id:
        try:
            user = Users.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False

def encrypt_pwd(pwd):
    return hashpw(b64encode(sha256(pwd.encode()).digest()), gensalt()).decode()

def check_pwd(x, y):
    """
    Check whether password hashed matches:
    * arg x** password to check
    * arg y** original hashed password
    """
    return checkpw(b64encode(sha256(x.encode()).digest()), y.encode())