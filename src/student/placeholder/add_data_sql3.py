"""
Code from COMP0035
Contains functions to add data to the paralympics database.
Uses sqlite3
"""
import sqlite3
from importlib import resources

import pandas as pd


def add_country_data(df, cursor, connection):
    """Add the country data to the paralympics database."""
    # Insert all values into the country table
    try:
        for index, row in df.iterrows():
            # The row is pandas series, we want the series as a list of values
            row_values = row.tolist()
            cursor.execute('INSERT INTO country VALUES (?,?,?,?,?,?)', row_values)

        connection.commit()

    except sqlite3.Error as e:
        print(f'An error occurred adding country data to the paralympics database. Error: {e}')
        if connection:
            connection.rollback()  # Rollback the changes on error


def add_event_data(df, cursor, connection):
    """Add event and participant data to the paralympics database."""
    try:
        # Convert the dates to strings
        df['start'] = df['start'].dt.strftime('%d/%m/%Y')
        df['end'] = df['end'].dt.strftime('%d/%m/%Y')

        # Insert the values into the event table
        for index, row in df.iterrows():
            values = (
                row['type'],
                row['year'],
                str(row['start']),
                str(row['end']),
                row['countries'],
                row['events'],
                row['sports'],
                row['highlights'],
                row['url'])
            cursor.execute(
                f'INSERT INTO event (type, year, start, end, countries, events, sports, highlights, url) VALUES (?, ? , ?, ?, ?, ?, ?, ?, ?)',
                values)
            # insert the participants data
            event_id = cursor.lastrowid
            participant_values = (
                event_id,
                row['participants_m'],
                row['participants_f'],
                row['participants'],
            )
            sql_ins_part = 'INSERT INTO participants (event_id, participants_m, participants_f, participants) VALUES (?, ?, ?, ?)'
            cursor.execute(sql_ins_part, participant_values)

        connection.commit()

    except sqlite3.Error as e:
        print(f'An error occurred adding event data to the paralympics database. Error: {e}')
        if connection:
            connection.rollback()


def add_host_data(df_events, cursor, connection):
    """Add data to the normalised paralympics database."""

    try:
        # Extract unique host and country pairs
        # Initialize an empty DataFrame with the columns needed
        host_country_df = pd.DataFrame(columns=['host', 'country'])
        # Iterate over each row in the events DataFrame and split each column into multiple values where there is ','
        for index, row in df_events.iterrows():
            hosts = row['host'].split(',')
            countries = row['country'].split(',')
            # Create pairs of each host with each country and append to the DataFrame
            for host, country in zip(hosts, countries):
                new_row = pd.DataFrame({'host': [host.strip()], 'country': [country.strip()]})
                host_country_df = pd.concat([host_country_df, new_row], ignore_index=True)
        # Remove duplicate hosts from the dataframe
        host_country_df = host_country_df.drop_duplicates(subset=['host', 'country'])

        # Iterate over the dataframe, add the host and country to the host table
        for index, row in host_country_df.iterrows():
            # Get the country code from the country table
            country_name = row['country']
            select_sql = f'SELECT code from country where name="{country_name}"'
            result = cursor.execute(select_sql).fetchone()
            country_code = result[0]
            # Insert into the host table
            host = row['host']
            cursor.execute('INSERT INTO host (country_code, host) VALUES (?, ?)', (country_code, host))

        # Commit the changes
        connection.commit()

    except sqlite3.Error as e:
        print(f'An error occurred adding host data to the paralympics database. Error: {e}')
        if connection:
            connection.rollback()  # Rollback the changes on error


def add_host_event_data(df, cursor, connection):
    """Add HostEvent data to the paralympics database."""

    try:
        # Iterate each event, find the pairs of hosts, then get the event_id and host_id and insert into the host_event table
        for index, row in df.iterrows():
            hosts = row['host'].split(',')
            # Find the event id for the event. This matches based on the year and type of event.
            event_id = cursor.execute(
                'SELECT event_id FROM event WHERE year = ? AND type = ?',
                (row['year'], row['type'])
            ).fetchone()[0]
            # Find the host_id for each host
            for host in hosts:
                host_id = cursor.execute(f'SELECT host_id FROM host WHERE host = "{host.strip()}"').fetchall()[0][0]
                # Insert the host_event pair
                cursor.execute('INSERT INTO host_event (host_id, event_id) VALUES (?, ?)', (host_id, event_id))

        connection.commit()

    except sqlite3.Error as e:
        print(f'An error occurred adding host_event data to the paralympics database. Error: {e}')
        if connection:
            connection.rollback()


def add_disabilities_data(df, cursor, connection):
    """Add Disability and DisabilityEvent data."""

    try:
        # Split the comma-separated values into lists
        split_disabilities = df['disabilities'].str.split(', ')
        # Flatten the list of lists into a single list
        all_disabilities = [item for sublist in split_disabilities for item in sublist]
        # Convert the list to a set to get unique values
        unique_disabilities = set(all_disabilities)
        # Insert the unique values into the table
        for d in unique_disabilities:
            cursor.execute('INSERT INTO disability (category) VALUES (?)', (d,))
        connection.commit()

        # Iterate each result row in the event table
        for index, row in df.iterrows():
            # find the event_id
            event_id = cursor.execute('SELECT event_id FROM event WHERE year = ? AND type = ?',
                                      (row['year'], row['type'])).fetchone()[0]
            # split the values for the disabilities
            disabilities = row['disabilities'].split(', ')
            # add each diability
            for d in disabilities:
                # find the disability_id.
                disability_id = cursor.execute(
                    'SELECT disability_id FROM disability WHERE category LIKE ?', (d,)
                ).fetchone()[0]
                # Insert into the DisabilityEvent table
                cursor.execute('INSERT INTO disability_event (event_id, disability_id) VALUES (?, ?)',
                               (event_id, disability_id))

        connection.commit()

    except sqlite3.Error as e:
        print(f'An error occurred adding disability data to the paralympics database. Error: {e}')
        if connection:
            connection.rollback()


def add_medal_result_data(df, cursor, connection):
    """Add MedalResult data to the paralympics database."""

    try:
        # Iterate each result row, get the event_id and code and insert into the MedalResult table
        for index, row in df.iterrows():
            # Find the event id for the event. This matches based on the year and type of event.
            qry = f'SELECT event_id FROM Event WHERE year = {row['Year']}'
            event_id = cursor.execute(qry).fetchone()[0]
            # Insert the medal results
            values = (event_id, row['NPC'], row['Rank'], row['Gold'], row['Silver'], row['Bronze'], row['Total'])
            sql = 'INSERT INTO medal_result (event_id, country_code, rank, gold, silver, bronze, total) VALUES (?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(sql, values)

        connection.commit()

    except sqlite3.Error as e:
        print(f'An error occurred adding MedalResult data. Error: {e}')
        if connection:
            connection.rollback()


def add_all_data(cur, conn):
    """Adds all the data.

    Parameters
    ----------
    conn: sqlite connection object
    cur: sqlite cursor object
    """
    # Specifies the path to the data file
    data_path = resources.files("tutor.data").joinpath("paralympics.xlsx")

    # Read data and create pandas dataframes
    events_df = pd.read_excel(data_path, sheet_name='events')
    medals_df = pd.read_excel(data_path, sheet_name='medal_standings')
    npc_df = pd.read_excel(data_path, sheet_name='npc_codes')

    # add data to the tables
    add_country_data(npc_df, cur, conn)
    add_host_data(events_df, cur, conn)
    add_event_data(events_df, cur, conn)
    add_host_event_data(events_df, cur, conn)
    add_disabilities_data(events_df, cur, conn)
    add_medal_result_data(medals_df, cur, conn)
