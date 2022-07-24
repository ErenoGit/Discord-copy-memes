# Discord copy memes system (WIP), for discord.js v14

Pre requirements: MySQL Database (with table "memes": BIGINT "ID" autoincrement, VARCHAR(200) "Link" UNIQUE), admin privileges on Discord server, Python (with mysql library), Node.js (with mysql library) version 16 or higher

System is divided into two parts: 
1. Python script that every X scrapes (using the discord token of the account that is on the source server) memes from the indicated channels and uploads links to memes to a MySQL database
and
2. Discord bot that every X downloads latest 50 memes from the MySQL database, checks if that memes have already been uploaded to the target channel, and if not, posts a link to the meme to target channel