CREATE TABLE game_rooms (id serial PRIMARY KEY, 
room_id VARCHAR (50),
player1 VARCHAR (50),
player2 VARCHAR (50),
created_on TIMESTAMP NOT NULL);
