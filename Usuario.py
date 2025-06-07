from pydantic import BaseModel
from typing import List, Optional

class UsuarioCreate(BaseModel):
    nome: str
    senha: str
    ultimo_login: str
    cargo: str

class Usuario(UsuarioCreate):
    id_usuario: int