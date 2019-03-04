CREATE TABLE users (
        id INTEGER NOT NULL, 
        login VARCHAR(20) NOT NULL, 
        money_amount INTEGER NOT NULL, 
        card_number VARCHAR(19) NOT NULL, 
        status BOOLEAN NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (login), 
        CHECK (status IN (0, 1))
);

CREATE TABLE p4$5w0rds (
    id       INTEGER PRIMARY KEY ASC ON CONFLICT REPLACE AUTOINCREMENT,
    password STRING
);

INSERT INTO users VALUES(1,'admin',1,'1111 0000 2222 3333',1);
INSERT INTO users VALUES(2,'use',1,'1111 0000 2222 3333',0);
INSERT INTO users VALUES(3,'test',0,'ABCDEF',1);
INSERT INTO users VALUES(4,'qwerty',1,'5430 3421 7621 6385',1);
INSERT INTO users VALUES(5,'wegsdfb',56,'5430342176216385',1);
INSERT INTO users VALUES(6,'Johnson',56,'5430342176218888',0);
INSERT INTO users VALUES(7,'Ben O''Connor',56,'5430342176218888',1);

INSERT INTO p4$5w0rds VALUES(1, 'test');
INSERT INTO p4$5w0rds VALUES(2, 'test');
INSERT INTO p4$5w0rds VALUES(3, 'test');
INSERT INTO p4$5w0rds VALUES(4, 'test');
INSERT INTO p4$5w0rds VALUES(5, 'test');
INSERT INTO p4$5w0rds VALUES(6, 'test');
INSERT INTO p4$5w0rds VALUES(7, 'test');

-- ############################### CENSORED ##################
-- ###########################################################
