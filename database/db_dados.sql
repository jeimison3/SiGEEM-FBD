BEGIN;

-- =========================
-- USUÁRIOS (18)
-- =========================
INSERT INTO Usuario (cpf, senha) VALUES
('111.111.111-11', 'hash1'),
('222.222.222-22', 'hash2'),
('333.333.333-33', 'hash3'),
('444.444.444-44', 'hash4'),
('555.555.555-55', 'hash5'),
('666.666.666-66', 'hash6'),
('777.777.777-77', 'hash7'),
('888.888.888-88', 'hash8'),
('999.999.999-99', 'hash9'),
('101.101.101-10', 'hash10'),
('202.202.202-20', 'hash11'),
('303.303.303-30', 'hash12'),
('404.404.404-40', 'hash13'),
('505.505.505-50', 'hash14'),
('606.606.606-60', 'hash15'),
('707.707.707-70', 'hash16'),
('808.808.808-80', 'hash17'),
('909.909.909-90', 'hash18');

-- =========================
-- ALUNOS (9)
-- =========================
INSERT INTO Aluno (
    matricula, nome_completo, data_nascimento,
    telefone_responsavel, ano_letivo, email, id_usuario
) VALUES
('A2024001', 'João Silva', '2008-05-10', '11990000001', 2024, 'joao@escola.com', 1),
('A2024002', 'Maria Santos', '2009-03-22', '11990000002', 2024, 'maria@escola.com', 2),
('A2024003', 'Pedro Oliveira', '2008-11-01', '11990000003', 2024, 'pedro@escola.com', 3),
('A2024004', 'Lucas Costa', '2009-02-18', '11990000004', 2024, 'lucas@escola.com', 7),
('A2024005', 'Ana Souza', '2008-08-09', '11990000005', 2024, 'ana@escola.com', 8),
('A2024006', 'Bruno Lima', '2009-12-30', '11990000006', 2024, 'bruno@escola.com', 9),
('A2024007', 'Paula Rocha', '2008-06-25', '11990000007', 2024, 'paula@escola.com', 10),
('A2024008', 'Rafael Mendes', '2009-01-14', '11990000008', 2024, 'rafael@escola.com', 11),
('A2024009', 'Camila Pires', '2008-10-03', '11990000009', 2024, 'camila@escola.com', 12);

-- =========================
-- PROFESSORES (6)
-- =========================
INSERT INTO Professor (
    nome_completo, data_nascimento, telefone,
    email, area_formacao, id_usuario
) VALUES
('Carlos Ferreira', '1980-02-15', '11980000001', 'carlos@escola.com', 'Matemática', 4),
('Ana Paula Lima', '1985-07-30', '11980000002', 'ana@escola.com', 'Português', 5),
('Marcos Teixeira', '1978-04-10', '11980000003', 'marcos@escola.com', 'Física', 13),
('Juliana Alves', '1983-09-22', '11980000004', 'juliana@escola.com', 'Química', 14),
('Ricardo Nunes', '1975-12-05', '11980000005', 'ricardo@escola.com', 'História', 15),
('Fernanda Lopes', '1988-01-19', '11980000006', 'fernanda@escola.com', 'Geografia', 16);

-- =========================
-- COORDENADORES (3)
-- =========================
INSERT INTO Coordenador (
    nome_completo, data_nascimento, telefone, email, id_usuario
) VALUES
('Roberto Alves', '1975-09-12', '11970000001', 'roberto@escola.com', 6),
('Helena Moraes', '1979-11-20', '11970000002', 'helena@escola.com', 17),
('Paulo Ribeiro', '1972-03-08', '11970000003', 'paulo@escola.com', 18);

-- =========================
-- DISCIPLINAS (6)
-- =========================
INSERT INTO Disciplina (nome_disciplina, carga_horaria) VALUES
('Matemática', 200),
('Português', 180),
('Física', 160),
('Química', 160),
('História', 140),
('Geografia', 140);

-- =========================
-- TURMAS (3)
-- =========================
INSERT INTO Turma (nome, sala) VALUES
('8º Ano A', '101'),
('8º Ano B', '102'),
('9º Ano A', '201');

-- =========================
-- PROFESSOR HABILITADO (12)
-- =========================
INSERT INTO Prof_Habilitado (id_professor, id_disciplina) VALUES
(1,1),(1,3),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(2,1),
(3,2),
(4,1),
(5,2),
(6,3);

-- =========================
-- AVALIAÇÕES (6)
-- =========================
INSERT INTO Avaliacao (
    nome_avaliacao, data_aplicacao, quanto_vale,
    peso, id_disciplina, id_turma, id_professor
) VALUES
('Prova Matemática 1', '2024-04-10', 10, 1, 1, 1, 1),
('Prova Português 1', '2024-04-12', 10, 1, 2, 1, 2),
('Prova Física 1', '2024-04-15', 10, 1, 3, 2, 3),
('Trabalho Química', '2024-04-18', 10, 1, 4, 2, 4),
('Seminário História', '2024-04-20', 10, 1, 5, 3, 5),
('Prova Geografia', '2024-04-22', 10, 1, 6, 3, 6);

-- =========================
-- AULAS (6)
-- =========================
INSERT INTO Aula (
    dt_hr_inicio, dt_hr_fim,
    id_disciplina, id_turma, id_professor
) VALUES
('2024-03-01 08:00', '2024-03-01 09:40', 1, 1, 1),
('2024-03-02 10:00', '2024-03-02 11:40', 2, 1, 2),
('2024-03-03 08:00', '2024-03-03 09:40', 3, 2, 3),
('2024-03-04 10:00', '2024-03-04 11:40', 4, 2, 4),
('2024-03-05 08:00', '2024-03-05 09:40', 5, 3, 5),
('2024-03-06 10:00', '2024-03-06 11:40', 6, 3, 6);

-- =========================
-- POSTS (6)
-- =========================
INSERT INTO Posts_Plataforma (
    titulo, conteudo, id_turma, id_disciplina, id_professor
) VALUES
('Aviso Prova Matemática', 'Estudem capítulos 1 e 2', 1, 1, 1),
('Leitura Português', 'Capítulo 3 do livro', 1, 2, 2),
('Física Experimental', 'Trazer calculadora', 2, 3, 3),
('Trabalho Química', 'Entrega semana que vem', 2, 4, 4),
('História Geral', 'Conteúdo da prova', 3, 5, 5),
('Mapa Geográfico', 'Atividade prática', 3, 6, 6);

-- =========================
-- INTERAÇÕES (6)
-- =========================
INSERT INTO Iteracao_Post (
    id_aluno, id_post, id_turma, id_disciplina, id_professor, comentario
) VALUES
(1,1,1,1,1,'A prova será com consulta?'),
(2,2,1,2,2,'Já comecei a leitura'),
(3,3,2,3,3,'Pode usar fórmula?'),
(4,4,2,4,4,'Qual o formato do trabalho?'),
(5,5,3,5,5,'Vai cair tudo?'),
(6,6,3,6,6,'Precisa de mapa impresso?');

-- =========================
-- NOTAS (18)
-- =========================
INSERT INTO Nota (
    id_turma, id_aluno, id_disciplina,
    id_professor, id_avaliacao, nota, peso
) VALUES
(1,1,1,1,1,8.5,1),
(1,2,1,1,1,9.0,1),
(1,3,1,1,1,7.5,1),
(1,4,2,2,2,8.0,1),
(1,5,2,2,2,9.2,1),
(1,6,2,2,2,6.8,1),
(2,7,3,3,3,7.0,1),
(2,8,3,3,3,8.1,1),
(2,9,3,3,3,9.4,1),
(2,1,4,4,4,8.3,1),
(2,2,4,4,4,7.9,1),
(2,3,4,4,4,6.5,1),
(3,4,5,5,5,9.0,1),
(3,5,5,5,5,8.8,1),
(3,6,5,5,5,7.6,1),
(3,7,6,6,6,8.4,1),
(3,8,6,6,6,9.1,1),
(3,9,6,6,6,7.2,1);

COMMIT;