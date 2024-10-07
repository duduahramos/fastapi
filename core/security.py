from passlib.context import CryptContext


CRYPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Função para verificar se a senha está correta, 
    compara a senha informada pelo usuario
    com o hash salvo no banco de dados.
    """

    return CRYPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    """
    Função que gera e retorna o a senha hashficada
    """

    return CRYPTO.hash(senha)
