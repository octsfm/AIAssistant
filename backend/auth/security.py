from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)


import os
import hmac

def generate_token() -> str:
    return hmac.new(
        os.urandom(32),
        os.urandom(32),
        'sha256'
    ).hexdigest()