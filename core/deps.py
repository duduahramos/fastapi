from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel


class TokenData(BaseModel):
    user_id: Optional[str] = None


async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()


async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_schema)) -> UsuarioModel:
    # instanciada um objeto da classe HTTPException, para diminuir código nos locais que esta excessão é levantada
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # decodifica o body do token jwt
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORTITHM],
            options={"verify_aud": False}
        )

        # captura do body o id do usuario e váldida se é válido
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credential_exception

        # instancia um objeto TokenData, passa o id do usuário como parâmetro
        token_data: TokenData = TokenData(user_id=user_id)
    except JWTError:
        raise credential_exception

    async with db as session:
        # busca o usuário no banco baseado no id capturado do body do token
        query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.user_id))
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if usuario is None:
            raise credential_exception

        return usuario
