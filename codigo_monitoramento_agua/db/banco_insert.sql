-- ===============================
-- INSERÇÃO DE DADOS DE TESTE
-- ===============================

-- 1️⃣ Usuários

INSERT INTO usuario (nome, email, senha)
VALUES 
('Maycon Fidelis', 'maycon@exemplo.com', 'senha_hash_exemplo'),
('Ana Silva', 'ana@exemplo.com', 'hash123'),
('Carlos Souza', 'carlos@exemplo.com', 'hash456');

-- 2️⃣ Áreas de Observação
INSERT INTO areas_de_observacao (nome, descricao, local)
VALUES 
('Lago Azul', 'Área principal de observação de qualidade da água', 'Região Norte'),
('Rio Verde', 'Região com grande fluxo hídrico e medições constantes', 'Região Leste');

-- 3️⃣ Subáreas
INSERT INTO subareas_de_observacao (area_de_observacao_id, nome, descricao, local)
VALUES
(1, 'Margem Norte', 'Área próxima às nascentes', 'Ponto A'),
(1, 'Centro do Lago', 'Área com maior profundidade', 'Ponto B'),
(2, 'Margem Sul', 'Área próxima à comunidade local', 'Ponto C');

-- 4️⃣ Medições (corrigido: antes “medicação”)
INSERT INTO medicacao (data, horario, subarea_observacao_id)
VALUES
('2025-10-06', '08:00:00', 1),
('2025-10-06', '09:00:00', 2),
('2025-10-06', '10:00:00', 3);

-- 5️⃣ Valores Medidos (Originais)
INSERT INTO valores_medidos_original (medicacao_id, ph, temperatura, turbidez, oxigenio_dissolvido)
VALUES
(1, 7.2, 24.5, 1.1, 8.0),
(2, 6.8, 25.1, 1.5, 7.5),
(3, 7.5, 23.8, 1.0, 8.2);

-- 6️⃣ Valores Medidos (Convertidos)
INSERT INTO valores_medidos_convertido (medicacao_id, ph, temperatura, turbidez, oxigenio_dissolvido)
VALUES
(1, 7.0, 24.7, 1.0, 8.1),
(2, 6.9, 25.0, 1.4, 7.6),
(3, 7.4, 23.9, 0.9, 8.3);

-- 7️⃣ Relacionamento Usuário ↔ Áreas
INSERT INTO usuario_areas (id_area, id_usuario)
VALUES
(1, 1),
(1, 2),
(2, 3);
