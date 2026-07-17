import hashlib


def gerar_md5(senha: str) -> str:
    """Converte a senha informada para MD5."""
    return hashlib.md5(
        senha.encode("utf-8"),
        usedforsecurity=False,
    ).hexdigest()