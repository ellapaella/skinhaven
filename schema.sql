
CREATE TABLE Users (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP DEFAULT NOW(), 
    username TEXT UNIQUE, 
    passhash TEXT, 
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Privmessages (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP DEFAULT NOW(), 
    creator_id INTEGER REFERENCES Users, 
    target_id INTEGER REFERENCES Users, 
    topic TEXT, 
    contents TEXT
);

CREATE TABLE Profiles (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP DEFAULT NOW(), 
    user_id INTEGER REFERENCES Users, 
    profile_name TEXT, 
    game_username TEXT, 
    game TEXT
);

CREATE TABLE Skins (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP DEFAULT NOW(), 
    creator_id INTEGER REFERENCES Users, 
    owner_id INTEGER REFERENCES Users, 
    profile_id INTEGER REFERENCES Profiles, 
    skin_name TEXT, 
    skin_price INTEGER
);

CREATE TABLE Threads (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP DEFAULT NOW(), 
    creator_id INTEGER REFERENCES Users, 
    topic TEXT
);
    
CREATE TABLE Threadmessages (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP DEFAULT NOW(), 
    creator_id INTEGER REFERENCES Users, 
    thread_id INTEGER REFERENCES Threads, 
    contents TEXT
);
