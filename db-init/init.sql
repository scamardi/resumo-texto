CREATE TABLE IF NOT EXISTS resumo (
    id SERIAL PRIMARY KEY,
    url VARCHAR(200) UNIQUE NOT NULL,
    resumo VARCHAR(10000) NOT NULL,
    palavras INTEGER NOT NULL
);

INSERT INTO resumo (url, resumo, palavras) VALUES
('https://www.wikipedia.org/teste', 'resumo teste', 2);