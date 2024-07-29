from fastapi import HTTPException, status


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

USER_EXCEPTION = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password.",
    headers={"WWW-Authenticate": "Bearer"},
)
