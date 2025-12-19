from fastapi import APIRouter
from pydantic import BaseModel
from app.core.security import create_toke

router = APIRouter()

class AuthInput(BaseModel):
    username : str
    password : str


@router.post('/login')
def login(auth: AuthInput):
    if (auth.username == "admin") and (auth.password == "admin"):
        token = create_toke({"sub" : auth})
        return {"access_toke" : token}
    return {"error" : "Invalid Credential"}
    
