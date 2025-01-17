# 3. Scatter Geo map

In this activity you will create
a [Plotly Express Scatter Geo](https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo.html?highlight=scatter_geo),
a world map with markers to show the location of each paralympic games. The data will be read into a pandas DataFrame from a
SQLite database file.

The map requires the latitude and longitude of each event. These have been added to the SQLite database in the `host`
table.

## Create the scatter geo

```python
import sqlite3
from importlib import resources

import pandas as pd
import plotly.express as px


def scatter_geo():
    with resources.path("data", "paralympics.db") as path:
        # create database connection
        connection = sqlite3.connect(path)

        # define the sql query
        sql = '''
        SELECT event.year, host.host, host.latitude, host.longitude FROM event
        JOIN host_event ON event.event_id = host_event.event_id
        JOIN host on host_event.host_id = host.host_id
        '''
        
        # Use pandas read_sql to run a sql query and access the results as a DataFrame
        df_locs = pd.read_sql(sql=sql, con=connection, index_col=None)
        
        # The lat and lon are stored as string but need to be floats for the scatter_geo
        df_locs['longitude'] = df_locs['longitude'].astype(float)
        df_locs['latitude'] = df_locs['latitude'].astype(float)
        
        # Adds a new column that concatenates the city and year e.g. Barcelona 2012
        df_locs['name'] = df_locs['host'] + ' ' + df_locs['year'].astype(str)
        
        # Create the figure
        fig = px.scatter_geo(df_locs,
                             lat=df_locs.latitude,
                             lon=df_locs.longitude,
                             hover_name=df_locs.name,
                             title="Where have the paralympics been held?",
                             )
        return fig
```

## Add the map to the layout
In paralympics_dash.py add code to create the figure using the function above, e.g.

```python
from dash_single.figures import scatter_geo

# Create the scatter map
map = scatter_geo()
```

In the layout add the `dcc.Graph()` component with the map and remove the placeholder image.

Run the app if not already running. You should see a map of the world with small dots for each event. When you hover on
a dot it will show the city and year.

## (Optional) Modify the styling of the markers
There are options for styling the markers, though this requires some Plotly Go syntax. Refer to the [Plotly maps
documentation](https://plotly.com/python/scatter-plots-on-maps/) if you want to try to change the marker styles.

[Next activity](2-5-stats-card.md)