from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from pydantic import EmailStr

from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verificar_senha


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    """
    Função que válida a tentativa de login
    """
    async with db as session:
        # busca o usuário pelo email informado
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario_db: UsuarioModel = result.scalars().unique().one_or_none()

        # se não encontrou, usuário provavelmente nao existe ou email esta errado
        if not usuario_db:
            return None

        # verifica se a senha da requisição bate com a senha cadastrada no banco
        if not verificar_senha(senha, usuario_db.senha):
            return None

        return usuario_db


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3 - para saber mais
    payload = {}

    sp = timezone("America/Sao_Paulo")
    expira = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)  # issued at/gerado em:
    payload["sub"] = str(sub)  # sujeito/usuario

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORTITHM)


def criar_token_acesso(sub: str) -> str:
    # https://jwt.io

    return _criar_token(
        tipo_token="access_token",
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
