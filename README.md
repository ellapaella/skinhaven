# Skinhaven

## A Collective place of discussion and trading for gaming skins

### On this site you can:

1. Create a user account for the hub
2. Discuss about gaming skins with other enthusiasts
3. Browse available skins
4. Buy skins from others, transfering the ownership to you
5. Sell your skins to others in a safe and secure way


The trading of skins is implemented on a 3rd party service provider and the site 
does not handle any payments or see payment details. The data is sent and verified 
to a collective skin and NFT database handler before any transaction is finished, 
to guarantee the safe transfer of ownership (note that this will not be implemented in reality).


### To do list ###

1. Skin handler, browsing skins and transfering ownership to other users
2. Private messaging between users
3. Page layout and cosmetic appearance


To test the program locally run the following commands:

First make sure you have installed `python3` and `postgresql` in your computer and then run the 
following in the command line (make sure you are in the desired folder where you want to test the 
program):

`git clone https://www.github.com/ellapaella/skinhaven`

This should produce the skinhaven folder. Traverse there with `cd skinhaven/`and do the following:


Create the python virtual environment

`python3 -m venv venv`

Launch the environment

`source venv/bin/activate`

Install necessary requirements

`pip install -r requirements.txt`

Now create a database for the project by logging into psql with the command 
(you must have created a user to the postgreql server first):

`psql`

Now run the following command replacing the "name_of_database" with a name of your choosing (i.e. 
skinhaven):

`CREATE DATABASE name_of_database;`

This should create a database for the project.

Now return to command line with the `\q` and feed your database with the schema.sql file you 
downloaded with the project. Use the following command (again inserting the name of database here, 
otherwise it will create the tables to your default database which most likely will be your username):

`psql name_of_database < schema.sql`

This creates the necessary tables for you to use the program locally.

Now add the following line to .env file in the project root and 
replace the "name_of_database" with the database name you created:

`DATABASE_URL=postgresql:///name_of_database`

You also have to make a secret key for user and account handling with the following commands.

First open the python interpreter in the command line

`python3`

Now produce the key with the following in the python interpreter:

`import secrets`

`secrets.token_hex(16)`

Copy the key and paste it in place of the "secret_key" and save the line (to it's own line) to the 
same .env file you created for the database address:

`SECRET_KEY=secret_key`

Now all the prerequisites should be done and you are ready to test the program by running

`flask run`

in the command line (be sure to have activated the python virtual environment) and going to the 
address 127.0.0.1:5000 with your browser
