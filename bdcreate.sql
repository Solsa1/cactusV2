CREATE TABLE IF NOT EXISTS empresa(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            jogo TEXT,
            logo TEXT,
            desc TEXT NOT NULL
)
    
CREATE TABLE IF NOT EXISTS jogo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empre INTEGER,
            nome TEXT UNIQUE,
            preco FLOAT NOT NULL,
            desc TEXT NOT NULL,
            foto TEXT NOT NULL,
            data_lancamento DATE,
            FOREIGN KEY(id_empre) REFERENCES empresa(id)
)
    
CREATE TABLE IF NOT EXISTS usuario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            foto TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS biblioteca(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_jogo INTEGER,
            id_user INTEGER,
            FOREIGN KEY(id_jogo) REFERENCES jogo(id),
            FOREIGN KEY(id_user) REFERENCES usuario(id)
  )
