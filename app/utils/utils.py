from passlib.context import CryptContext
pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    hashed_password = pwd_contex.hash(password)
    return hashed_password

def veriy(plain_password: str, hashed_password):
    return pwd_contex.verify(plain_password, hashed_password)