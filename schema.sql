
CREATE TABLE Users (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP DEFAULT NOW(), 
    username TEXT UNIQUE, 
    passhash TEXT, 
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Profiles (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP, 
    user_id INTEGER REFERENCES Users, 
    profile_number INTEGER, 
    profilename TEXT, 
    game TEXT
);

CREATE TABLE Skins (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP, 
    creator_id INTEGER REFERENCES Users, 
    owner_id INTEGER REFERENCES Users, 
    profile_id INTEGER REFERENCES Profiles, 
    skin_name TEXT, 
    skin_price INTEGER
);

CREATE TABLE Threads (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP, 
    creator_id INTEGER REFERENCES Users, 
    topic TEXT
);
    
CREATE TABLE Messages (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP, 
    creator_id INTEGER REFERENCES Users, 
    creator TEXT, 
    thread_id INTEGER REFERENCES Threads, 
    content TEXT
);

CREATE TABLE Privmessages (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP, 
    creator_id INTEGER REFERENCES Users, 
    target_id INTEGER REFERENCES Users, 
    content TEXT
);