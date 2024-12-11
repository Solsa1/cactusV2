create table if not exists empresa(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            logo TEXT,
            descricao TEXT NOT NULL
);
    
create table if not exists jogo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empre INTEGER,
            nome TEXT UNIQUE,
            preco FLOAT NOT NULL,
            descricao TEXT NOT NULL,
            foto TEXT NOT NULL,
            data_lancamento DATE,
            FOREIGN KEY(id_empre) REFERENCES empresa(id)
);
    
create table if not exists usuario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            foto TEXT NOT NULL
);

create table if not exists biblioteca(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_jogo INTEGER,
            id_user INTEGER,
            FOREIGN KEY(id_jogo) REFERENCES jogo(id),
            FOREIGN KEY(id_user) REFERENCES usuario(id)
);

create table if not exists vendas(
            id integer PRIMARY KEY AUTOINCREMENT,
            id_jogo INTEGER,
            id_comprador INTEGER,
            id_vendedor INTEGER,
            FOREIGN KEY(id_jogo) REFERENCES jogo(id),
            FOREIGN KEY(id_comprador) REFERENCES usuario(id),
            FOREIGN KEY(id_vendedor) REFERENCES empresa(id)
);

