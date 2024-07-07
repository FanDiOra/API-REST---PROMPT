-- Connexion à la base de données
\c projet_api_rest_bd;

-- Création du type ENUM pour le rôle
CREATE TYPE user_role AS ENUM ('admin', 'user');

-- Création des tables
CREATE TABLE "group" (
    groupID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE "user" (
    userID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    login VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role user_role NOT NULL,
    groupID INT,
    FOREIGN KEY (groupID) REFERENCES "group" (groupID)
);

CREATE TABLE "prompt" (
    promptID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content TEXT NOT NULL,
    status VARCHAR(64) NOT NULL,
    price FLOAT DEFAULT 1000,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES "user" (userID)
);

CREATE TABLE "vote" (
    voteID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    vote_value INT NOT NULL,
    user_id INT,
    prompt_id INT,
    FOREIGN KEY (user_id) REFERENCES "user" (userID),
    FOREIGN KEY (prompt_id) REFERENCES "prompt" (promptID)
);

CREATE TABLE "note" (
    noteID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    note_value FLOAT NOT NULL,
    user_id INT,
    prompt_id INT,
    FOREIGN KEY (user_id) REFERENCES "user" (userID),
    FOREIGN KEY (prompt_id) REFERENCES "prompt" (promptID)
);
