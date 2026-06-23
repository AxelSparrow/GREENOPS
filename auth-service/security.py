from jose import jwt, JWTError
import bcrypt

SECRET_KEY = "greenops-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None
    
def hash_password(password: str):

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verify_password(
    plain_password: str,
    hashed_password: str
):

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
   