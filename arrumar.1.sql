USE escola_db;

TRUNCATE TABLE usuarios;

INSERT INTO usuarios
(nome, usuario, senha_md5)
VALUES
(
    'Administrador do Sistema',
    'admin',
    MD5('admin123')
);