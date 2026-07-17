DROP USER IF EXISTS 'escola_app'@'localhost';
DROP USER IF EXISTS 'escola_app'@'127.0.0.1';

CREATE USER 'escola_app'@'localhost'
IDENTIFIED BY 'Escola2026';

CREATE USER 'escola_app'@'127.0.0.1'
IDENTIFIED BY 'Escola2026';

GRANT ALL PRIVILEGES ON escola_db.*
TO 'escola_app'@'localhost';

GRANT ALL PRIVILEGES ON escola_db.*
TO 'escola_app'@'127.0.0.1';

FLUSH PRIVILEGES;