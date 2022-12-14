import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    convert the JSON files into DataFrame then Select the related song data from the DataFrame and place it into 'songs' table,
    then Select the related User data from the DataFrame and place it into 'artists' table.
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = (df[["song_id", "title", "artist_id", "year", "duration"]].values.tolist()[0])
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = (df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values.tolist()[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    convert the JSON files into DataFrame then Filter records by NextSong,
    Convert the ts timestamp column to DateTime, Extract the timestamp, hour, day, week of year, month, year, and weekday
    from the ts column into new columns, then Create a data frame from the columns these columns called time_df, then insert each row INTO
    the user and songplay tables
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query("page == 'NextSong'")

    # convert timestamp column to datetime
    df["ts"] = pd.to_datetime(df["ts"], unit='ms')

    # covert datetime to day,week,hour,month,year,weekday and insert them into columns in df dataframe
    df["weekday"] = df["ts"].dt.day_of_week
    df["hour"] = df["ts"].dt.hour
    df["day"] = df["ts"].dt.day
    df["month"] = df["ts"].dt.month
    df["year"] = df["ts"].dt.year
    df["week"] = df["ts"].dt.isocalendar().week

    # copy time data records into new data frame
    time_df = df[['ts', 'hour', 'day', 'week', 'month', 'year', 'weekday']].copy()

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]].copy()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: This function can be used to read the file in the filepath (data/log_data)
    to get the user and time info and used to populate the users and time dim tables.

    Arguments:
        cur: the cursor object.
        filepath: log data file path.

        Returns: None
        """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
