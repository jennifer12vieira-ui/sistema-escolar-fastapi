from sqlalchemy import text

from app.database import engine


def testar_conexao():
    try:
        with engine.connect() as conexao:
            resultado = conexao.execute(
                text("SELECT DATABASE() AS banco, VERSION() AS versao")
            ).mappings().one()

            print("Conexão realizada com sucesso!")
            print(f"Banco conectado: {resultado['banco']}")
            print(f"Versão do MySQL: {resultado['versao']}")

    except Exception as erro:
        print("Não foi possível conectar ao banco.")
        print(f"Erro: {erro}")


if __name__ == "__main__":
    testar_conexao()