CREATE DATABASE IF NOT EXISTS escola_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE escola_db;

CREATE TABLE alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    rua VARCHAR(150) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

CREATE TABLE professores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    rua VARCHAR(150) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

CREATE TABLE disciplinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    horario VARCHAR(100) NOT NULL,
    professor_id INT NOT NULL,

    CONSTRAINT fk_disciplina_professor
        FOREIGN KEY (professor_id)
        REFERENCES professores(id)
);

CREATE TABLE matriculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT NOT NULL,
    disciplina_id INT NOT NULL,
    nota1 DECIMAL(4,2) NOT NULL DEFAULT 0,
    nota2 DECIMAL(4,2) NOT NULL DEFAULT 0,
    nota3 DECIMAL(4,2) NOT NULL DEFAULT 0,
    nota4 DECIMAL(4,2) NOT NULL DEFAULT 0,

    CONSTRAINT aluno_disciplina_unico
        UNIQUE (aluno_id, disciplina_id),

    CONSTRAINT fk_matricula_aluno
        FOREIGN KEY (aluno_id)
        REFERENCES alunos(id),

    CONSTRAINT fk_matricula_disciplina
        FOREIGN KEY (disciplina_id)
        REFERENCES disciplinas(id)
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    senha_md5 CHAR(32) NOT NULL
);