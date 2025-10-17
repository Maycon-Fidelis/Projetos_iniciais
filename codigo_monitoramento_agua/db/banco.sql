-- Criação do banco
CREATE DATABASE monitoramento_agua;

-- Criação das tabelas
CREATE TABLE areas_de_observacao 
( 
    id SERIAL PRIMARY KEY,  
    nome VARCHAR(100) NOT NULL,  
    descricao TEXT,  
    local VARCHAR(100),
    id_area_pai INT,
    FOREIGN KEY (id_area_pai) REFERENCES areas_de_observacao(id) ON DELETE SET NULL
);  


CREATE TABLE subareas_de_observacao 
( 
    id SERIAL PRIMARY KEY,  
    area_de_observacao_id INT NOT NULL,  
    nome VARCHAR(100) NOT NULL,  
    descricao TEXT,  
    local VARCHAR(100),
    FOREIGN KEY (area_de_observacao_id) REFERENCES areas_de_observacao(id) ON DELETE CASCADE
);


CREATE TABLE medicacao 
( 
    id SERIAL PRIMARY KEY,  
    data DATE NOT NULL,  
    horario TIME NOT NULL,  
    subarea_observacao_id INT NOT NULL,
    FOREIGN KEY (subarea_observacao_id) REFERENCES subareas_de_observacao(id) ON DELETE CASCADE
);


CREATE TABLE valores_medidos_original 
( 
    id SERIAL PRIMARY KEY,
    medicacao_id INT NOT NULL,
    ph REAL,  
    temperatura REAL,  
    turbidez REAL,  
    oxigenio_dissolvido REAL,
    FOREIGN KEY (medicacao_id) REFERENCES medicacao(id) ON DELETE CASCADE
);

CREATE TABLE valores_medidos_convertido 
( 
    id SERIAL PRIMARY KEY,
    medicacao_id INT,  
    ph REAL,  
    turbidez REAL,  
    temperatura REAL,  
    oxigenio_dissolvido REAL,
    FOREIGN KEY (medicacao_id) REFERENCES medicacao(id)
);

CREATE TABLE usuario 
( 
    id SERIAL PRIMARY KEY,  
    nome VARCHAR(100) NOT NULL,  
    email VARCHAR(100) UNIQUE NOT NULL,  
    senha VARCHAR(255) NOT NULL  
);

CREATE TABLE usuario_areas 
( 
    id SERIAL PRIMARY KEY,
    id_area INT NOT NULL,  
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_area) REFERENCES areas_de_observacao(id) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
    UNIQUE (id_area, id_usuario)
);

-- Chave estrangeira recursiva (área pode ter uma "área pai")
ALTER TABLE areas_de_observacao 
    ADD FOREIGN KEY (id_area_pai) REFERENCES areas_de_observacao(id);
