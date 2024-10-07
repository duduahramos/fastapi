from typing import Optional, List
from pydantic import BaseModel, EmailStr

from .artigo_schema import ArtigoSchema


# schema usado para retornar uma lista de usuarios, exemplo um tela de conmsulta geral de usuarios, sem muitas infos
class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    admin: bool = False

    class Config:
        orm_mode = True


# schema usado para retornar 1 único usuário, exemplo tela de cadastro do usuário
class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


# schema para uma busca de artigos por usuários
class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]


# schema para um update de usuario
class UsuarioschemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    admin: Optional[bool]
