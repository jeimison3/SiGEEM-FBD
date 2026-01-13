CREATE DATABASE SIGEEM;

-- TABELAS DE USUÁRIOS
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario SERIAL PRIMARY KEY,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    senha VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS Aluno (
    id_aluno SERIAL PRIMARY KEY,
    matricula VARCHAR(20) UNIQUE,
    nome_completo VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone_responsavel VARCHAR(20) NOT NULL,
    ano_letivo INT,
    email VARCHAR(100) UNIQUE,
    id_usuario INT UNIQUE NOT NULL,
    CONSTRAINT fk_aluno_usuario FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS Professor (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    area_formacao VARCHAR(100) NOT NULL,
    id_usuario INT UNIQUE NOT NULL,
    CONSTRAINT fk_prof_usuario FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS Coordenador (
    id_coordenador SERIAL PRIMARY KEY,
    nome_completo VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    id_usuario INT UNIQUE NOT NULL,
    CONSTRAINT fk_coord_usuario FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
);

-- TABELAS DE RELACIONAMENTO
CREATE TABLE IF NOT EXISTS Disciplina (
    id_disciplina SERIAL PRIMARY KEY,
    nome_disciplina VARCHAR(100),
    carga_horaria INT NOT NULL,
    obrigatoriedade BOOLEAN DEFAULT TRUE,
    ativa BOOLEAN DEFAULT TRUE,
    prerequisito INT,
    CONSTRAINT fk_disciplina_prerequisito FOREIGN KEY (prerequisito)
    REFERENCES Disciplina(id_disciplina)
);

CREATE TABLE IF NOT EXISTS Turma (
    id_turma SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    sala VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS Parametros_Gerais (
    chave_parametro VARCHAR(50) PRIMARY KEY,
    valor_parametro TEXT,
    data_ultima_atualizacao DATE
);

CREATE TABLE IF NOT EXISTS Prof_Habilitado (
    id_professor INT NOT NULL,
    id_disciplina INT NOT NULL,
    PRIMARY KEY (id_professor, id_disciplina),
    CONSTRAINT fk_const_professor FOREIGN KEY (id_professor)
    REFERENCES Professor(id_professor),
    CONSTRAINT fk_const_disciplina FOREIGN KEY (id_disciplina)
    REFERENCES Disciplina(id_disciplina)
);

CREATE TABLE IF NOT EXISTS Avaliacao (
    id_avaliacao SERIAL PRIMARY KEY,
    nome_avaliacao VARCHAR(100) NOT NULL,
    data_aplicacao DATE DEFAULT CURRENT_DATE,
    quanto_vale NUMERIC(5, 2),
    peso NUMERIC(5, 2),
    id_disciplina INT NOT NULL,
    id_turma INT NOT NULL,
    id_professor INT NOT NULL,
    CONSTRAINT fk_avaliacao_disciplina FOREIGN KEY (id_disciplina)
    REFERENCES Disciplina(id_disciplina),
    CONSTRAINT fk_avaliacao_turma FOREIGN KEY (id_turma)
    REFERENCES Turma(id_turma),
    CONSTRAINT fk_avaliacao_professor FOREIGN KEY (id_professor)
    REFERENCES Professor(id_professor)
);

CREATE TABLE IF NOT EXISTS Aula (
    id_aula SERIAL PRIMARY KEY,
    dt_hr_inicio TIMESTAMP NOT NULL,
    dt_hr_fim TIMESTAMP NOT NULL,
    id_disciplina INT NOT NULL,
    id_turma INT NOT NULL,
    id_professor INT NOT NULL,
    CONSTRAINT fk_aula_disciplina FOREIGN KEY (id_disciplina)
    REFERENCES Disciplina (id_disciplina),
    CONSTRAINT fk_aula_turma FOREIGN KEY (id_turma)
    REFERENCES Turma (id_turma),
    CONSTRAINT fk_aula_professor FOREIGN KEY (id_professor)
    REFERENCES Professor (id_professor)
);

-- TABELAS DE POSTS
CREATE TABLE IF NOT EXISTS Posts_Plataforma (
    id_post SERIAL,
    titulo VARCHAR(100),
    conteudo TEXT,
    id_turma INT NOT NULL,
    id_disciplina INT NOT NULL,
    id_professor INT NOT NULL,
    PRIMARY KEY (id_post, id_turma, id_disciplina, id_professor),
    CONSTRAINT fk_posts_turma FOREIGN KEY (id_turma)
    REFERENCES Turma (id_turma),
    CONSTRAINT fk_posts_disciplina FOREIGN KEY (id_disciplina)
    REFERENCES Disciplina (id_disciplina),
    CONSTRAINT fk_posts_professor FOREIGN KEY (id_professor)
    REFERENCES Professor (id_professor)
);


CREATE TABLE IF NOT EXISTS Iteracao_Post (
    id_interacao SERIAL,
    id_aluno INT NOT NULL,
    id_post INT NOT NULL,
    id_turma INT NOT NULL,
    id_disciplina INT NOT NULL,
    id_professor INT NOT NULL,
    comentario TEXT,
    PRIMARY KEY (id_interacao, id_aluno, id_post, id_turma, id_disciplina, id_professor),
    CONSTRAINT fk_interacao_aluno FOREIGN KEY (id_aluno)
    REFERENCES Aluno(id_aluno),
    CONSTRAINT fk_interacao_posts FOREIGN KEY (id_post, id_turma, id_disciplina, id_professor)
    REFERENCES Posts_Plataforma(id_post, id_turma, id_disciplina, id_professor)
);

-- TABELAS DE NOTAS
CREATE TABLE IF NOT EXISTS Nota (
    id_turma INT NOT NULL,
    id_aluno INT NOT NULL,
    id_disciplina INT NOT NULL,
    id_professor INT NOT NULL,
    id_avaliacao INT NOT NULL,
    nota NUMERIC(5, 2),
    peso NUMERIC(5, 2),
    PRIMARY KEY (id_turma, id_aluno, id_disciplina, id_professor, id_avaliacao),
    CONSTRAINT fk_nota_turma FOREIGN KEY (id_turma)
    REFERENCES Turma(id_turma),
    CONSTRAINT fk_nota_aluno FOREIGN KEY (id_aluno)
    REFERENCES Aluno(id_aluno),
    CONSTRAINT fk_nota_disciplina FOREIGN KEY (id_disciplina)
    REFERENCES Disciplina(id_disciplina),
    CONSTRAINT fk_nota_professor FOREIGN KEY (id_professor)
    REFERENCES Professor(id_professor),
    CONSTRAINT fk_nota_avaliacao FOREIGN KEY (id_avaliacao)
    REFERENCES Avaliacao(id_avaliacao)
);


-- Valores:

DELETE FROM Usuario;
INSERT INTO Usuario (id_usuario, cpf, senha) VALUES 
(1,'11111111101', 'senha_aluno1'), (2, '11111111102', 'senha_aluno2'), (3, '11111111103', 'senha_aluno3'),
(4, '11111111104', 'senha_aluno4'), (5, '11111111105', 'senha_aluno5'), (6, '11111111106', 'senha_aluno6'),
(7, '11111111107', 'senha_aluno7'), (8, '11111111108', 'senha_aluno8'), (9, '11111111109', 'senha_aluno9'),
(10, '11111111110', 'senha_aluno10'),

(11, '22222222211', 'senha_prof1'), (12, '22222222212', 'senha_prof2'), (13, '22222222213', 'senha_prof3'),
(14, '22222222214', 'senha_prof4'), (15, '22222222215', 'senha_prof5'), (16, '22222222216', 'senha_prof6'),
(17, '22222222217', 'senha_prof7'), (18, '22222222218', 'senha_prof8'), (19, '22222222219', 'senha_prof9'),
(20, '22222222220', 'senha_prof10'), 

(21, '33333333321', 'senha_coord1'), (22, '33333333322', 'senha_coord2'), (23, '33333333323', 'senha_coord3'),
(24, '33333333324', 'senha_coord4'), (25, '33333333325', 'senha_coord5'), (26, '33333333326', 'senha_coord6'),
(27, '33333333327', 'senha_coord7'), (28, '33333333328', 'senha_coord8'), (29, '33333333329', 'senha_coord9'),
(30, '33333333330', 'senha_coord10');

INSERT INTO Aluno (matricula, nome_completo, data_nascimento, telefone_responsavel, ano_letivo, email, id_usuario)
VALUES 
('UUID_MATRIC01', 'Joao Pereira', '2005-01-15', '88991112233', 1, 'joao.p@alu.escola.com', 1),
('UUID_MATRIC02', 'Maria Souza', '2004-11-20', '88992223344', 2, 'maria.s@alu.escola.com', 2),
('UUID_MATRIC03', 'Carlos Lima', '2006-03-01', '88993334455', 1, 'carlos.l@alu.escola.com', 3),
('UUID_MATRIC04', 'Ana Costa', '2005-07-10', '88994445566', 3, 'ana.c@alu.escola.com', 4),
('UUID_MATRIC05', 'Pedro Santos', '2003-09-25', '88995556677', 4, 'pedro.sa@alu.escola.com', 5),
('UUID_MATRIC06', 'Sofia Rocha', '2006-04-18', '88996667788', 2, 'sofia.r@alu.escola.com', 6),
('UUID_MATRIC07', 'Miguel Alves', '2004-02-28', '88997778899', 3, 'miguel.a@alu.escola.com', 7),
('UUID_MATRIC08', 'Laura Gomes', '2007-06-05', '88998889900', 1, 'laura.g@alu.escola.com', 8),
('UUID_MATRIC09', 'Davi Ferreira', '2003-12-12', '88999990011', 4, 'davi.f@alu.escola.com', 9),
('UUID_MATRIC10', 'Julia Oliveira', '2005-08-30', '88990001122', 2, 'julia.o@alu.escola.com', 10);

INSERT INTO Professor (nome_completo, data_nascimento, telefone, email, area_formacao, id_usuario)
VALUES
('Prof. Ana Mendes', '1975-03-05', '85981112233', 'ana.m@escola.com', 'Matemática', 11),
('Prof. Bruno Teixeira', '1982-11-12', '85982223344', 'bruno.t@escola.com', 'Português', 12),
('Prof. Clara Nunes', '1968-07-22', '85983334455', 'clara.n@escola.com', 'História', 13),
('Prof. Daniel Silva', '1990-01-29', '85984445566', 'daniel.s@escola.com', 'Geografia', 14),
('Prof. Elisa Guedes', '1985-04-14', '85985556677', 'elisa.g@escola.com', 'Ciências', 15),
('Prof. Fernando Cruz', '1978-08-08', '85986667788', 'fernando.c@escola.com', 'Física', 16),
('Prof. Giselle Paz', '1989-10-17', '85987778899', 'giselle.p@escola.com', 'Química', 17),
('Prof. Henrique Melo', '1972-02-24', '85988889900', 'henrique.m@escola.com', 'Literatura', 18),
('Prof. Isabela Reis', '1995-06-03', '85989990011', 'isabela.r@escola.com', 'Inglês', 19),
('Prof. Jorge Nogueira', '1981-12-09', '85980001122', 'jorge.n@escola.com', 'Filosofia', 20);

INSERT INTO Coordenador (nome_completo, data_nascimento, telefone, email, id_usuario)
VALUES
('Coord. Márcia Oliveira', '1965-09-01', '85991113355', 'marcia.o@escola.com', 21),
('Coord. Ricardo Pires', '1970-11-28', '85992224466', 'ricardo.p@escola.com', 22),
('Coord. Patrícia Gomes', '1980-04-10', '85993335577', 'patricia.g@escola.com', 23),
('Coord. Wagner Souza', '1973-01-08', '85994446688', 'wagner.s@escola.com', 24),
('Coord. Helena Ferreira', '1962-05-19', '85995557799', 'helena.f@escola.com', 25),
('Coord. Ivan Campos', '1988-08-21', '85996668800', 'ivan.c@escola.com', 26),
('Coord. Renata Borges', '1979-10-27', '85997779911', 'renata.b@escola.com', 27),
('Coord. Arthur Dias', '1960-03-16', '85998880022', 'arthur.d@escola.com', 28),
('Coord. Lúcia Barbosa', '1977-12-07', '85999991133', 'lucia.b@escola.com', 29),
('Coord. Marcelo Mota', '1983-06-02', '85990002244', 'marcelo.m@escola.com', 30);

-- 
