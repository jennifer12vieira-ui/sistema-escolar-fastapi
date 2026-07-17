USE escola_db;

-- PROFESSORES
INSERT INTO professores
(nome, rua, numero, bairro, cidade, estado, telefone)
VALUES
('Carlos Roberto Silva', 'Rua das Flores', '120', 'Centro',
 'Campinas', 'SP', '(19) 99911-1111'),

('Mariana Oliveira Souza', 'Avenida Brasil', '450', 'Jardim América',
 'Campinas', 'SP', '(19) 99922-2222'),

('Fernando Santos Lima', 'Rua dos Ipês', '75', 'Vila Nova',
 'Valinhos', 'SP', '(19) 99933-3333');


-- ALUNOS
INSERT INTO alunos
(nome, rua, numero, bairro, cidade, estado, telefone)
VALUES
('Julia Aparecida Pereira', 'Rua A', '10', 'Centro',
 'Campinas', 'SP', '(19) 98811-1111'),

('Jakson Felix', 'Rua B', '25', 'Taquaral',
 'Campinas', 'SP', '(19) 98822-2222'),

('Camile Vitoria Macedo Alves', 'Rua C', '100', 'Cambuí',
 'Campinas', 'SP', '(19) 98833-3333'),

('Daniel Alves Martins', 'Rua D', '55', 'Centro',
 'Valinhos', 'SP', '(19) 98844-4444'),

('Eduarda Gomes Ribeiro', 'Rua E', '230', 'Vila Industrial',
 'Campinas', 'SP', '(19) 98855-5555');


-- DISCIPLINAS
INSERT INTO disciplinas
(nome, horario, professor_id)
VALUES
('Matemática', 'Segunda-feira, das 19:00 às 21:00', 1),

('Programação em Python', 'Terça-feira, das 19:00 às 21:00', 2),

('Banco de Dados', 'Quarta-feira, das 19:00 às 21:00', 2),

('Eletricidade Básica', 'Quinta-feira, das 19:00 às 21:00', 3);


-- MATRÍCULAS E NOTAS
INSERT INTO matriculas
(aluno_id, disciplina_id, nota1, nota2, nota3, nota4)
VALUES
(1, 1, 8.00, 7.50, 9.00, 8.50),
(1, 2, 9.00, 8.50, 9.50, 10.00),

(2, 1, 5.00, 6.00, 5.50, 7.00),
(2, 3, 7.00, 8.00, 6.50, 7.50),

(3, 2, 10.00, 9.00, 9.50, 10.00),
(3, 3, 8.00, 8.50, 9.00, 9.50),

(4, 1, 4.00, 5.00, 4.50, 5.50),
(4, 4, 7.00, 7.50, 8.00, 8.50),

(5, 2, 6.00, 7.00, 8.00, 7.50),
(5, 4, 9.00, 8.50, 9.50, 10.00);


-- USUÁRIO DO SISTEMA
-- Usuário: admin Senha: admin123
USE escola_db;

UPDATE usuarios
SET
    nome = 'Administrador do Sistema',
    usuario = 'admin',
    senha_md5 = MD5('admin123')
WHERE id = 1;