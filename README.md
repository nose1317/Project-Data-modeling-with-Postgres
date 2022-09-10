# Project: Data modeling with Postgres
## Project summary
The purpose of the project is to create a Postgres database called **sparkifydb** , that takes its data from the song and log datasets (JSON format) to make a star schema for song play analysis queries, the star schema has 4 dimension tables (users, songs, artists, time), and 1 fact table (songplays)

## Explanation of the files in the repository
`create_tables.py` uses functions create_database, drop_tables, and create_tables which these functions are defined in `sql_queries.py`.

`etl.ipynb` reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.

`etl.py` reads and processes files from song_data and log_data and loads them into your tables. You can fill this out based on your work in the ETL notebook.

## Tables
#### Fact Table
1. songplays - records in log data associated with song plays i.e. records with page NextSong
• songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
#### Dimension Tables
2. users - users in the app
• user_id, first_name, last_name, gender, level
3. songs - songs in the music database
• song_id, title, artist_id, year, duration
4. artists - artists in the music database
• artist_id, name, location, latitude, longitude
5. time - timestamps of records in songplays broken down into specific units
• start_time, hour, day, week, month, year, weekday

## Instructions
Run `create_tables.py` to drop and create the tables.
Run `etl.py` to reads and process files from song_data and log_data and loads them into the tables.
Run `test.ipynb` to display the first few rows of each table to check the database.
