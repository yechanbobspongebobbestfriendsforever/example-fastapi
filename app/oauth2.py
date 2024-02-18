from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings



########################### NOTES ###############################
# Two main ways to tackle authentication
#  1. session based authentication
#  - we store something on our backend server or API to track whether a user is logged in
#  2. JWT based authentication
#  - stateless: there is nothing on our backend, API, or database that actually keeps track or stores some sort of information about whether a user is logged in or logged out
#  - JWT token itself, which we store in the frontend(client) keep track whether user is logged in or not

#environment variable: variable that you configure on a computer - any application thats running on that computer will be able to access it.


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

## 3 things to provide
# 1. SECRETE_KEY: special key that ultimately handles verifying the data integrity of our token
# 2. Algorithm: hash algorithm
# 3. Expiration time

# SECRETE_KEY = '09d25e094faa6ca2556c818166b7a9563b93f709'
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

SECRETE_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    encode_jwt = jwt.encode(claims=to_encode,
                            key=SECRETE_KEY, 
                            algorithm=ALGORITHM)
    
    return encode_jwt
    
def verify_access_token(token:str, credential_exception):
    try:
        payload = jwt.decode(
            token,
            SECRETE_KEY,
            algorithms=[ALGORITHM]
        )

        id: str = str(payload.get("user_id"))
        
        if id is None:
            raise credential_exception

        token_data = schemas.TokenData(id=id)
        
    except JWTError as e:
        raise credential_exception
        
    return token_data
        
        
def get_current_user(
    token:str=Depends(oauth2_scheme), 
    db: Session=Depends(database.get_db)
    ):
    # Pass this function as a dependency into any of our path operation. 
    # And when we do that, it's going to take the token from the request, verify if token is correct, extract the ID for us.
    # And if we want to, we can have it automatically fetch the user and add it as a parameter into out path operation function
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f'could not validate credentials',
        headers={"WWW-Authenticate":"Bearer"}
    )
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user