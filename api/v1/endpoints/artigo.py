from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema
from core.deps import get_session, get_current_user


router = APIRouter()

# post artigo
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_artigo: ArtigoModel = ArtigoModel(
        titulo=artigo.titulo,
        descricao=artigo.descricao,
        url_fonte=artigo.url_fonte,
        usuario_id=artigo.usuario_id
    )
    
    async with db as session:
        session.add(novo_artigo)
        await session.commit()  

    return novo_artigo


# get artigos
@router.get("/", response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()

        return artigos


# get artigo
@router.get("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail="Artigo não encontrado", status_code=status.HTTP_404_NOT_FOUND)


# put artigo
@router.put("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(artigo_id: int, artigo: ArtigoSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_db: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo_db:
            if artigo.titulo:
                artigo_db.titulo = artigo.titulo

            if artigo.descricao:
                artigo_db.descricao = artigo.descricao

            if artigo.url_fonte:
                artigo_db.url_fonte = artigo.url_fonte

            # se o usuário logado for diferente do usuário que criou o artigo, atualiza o usuário do artigo
            # exemplo: um usuario X percebe que o usuário Y criou um artigo com informações erradas, 
            # então o usuário X atualiza o artigo e vira o dono do artigo
            if usuario_logado.id != artigo_db.usuario_id:
                artigo_db.usuario_id = usuario_logado.id
            
            await session.commit()
            
            return artigo_db
        else:
            raise HTTPException(detail="Artigo não encontrado", status_code=status.HTTP_404_NOT_FOUND)


# delete artigo
@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_db: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo_db:
            if usuario_logado.id != artigo_db.usuario_id:
                raise HTTPException(detail="Usuário logado não é o mesmo que criou o artigo.", status_code=status.HTTP_403_FORBIDDEN)

            await session.delete(artigo_db)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Artigo não encontrado", status_code=status.HTTP_404_NOT_FOUND)
