# 2. Bar chart

In this activity you will create a bar chart using Plotly Express. The data will be read into a pandas DataFrame from a 
`.csv` file.

## Code to create the bar chart

Create a stacked [bar chart](https://plotly.com/python-api-reference/generated/plotly.express.bar.html) that shows the
ratio of female:male competitors for either winter or summer events.

This requires manipulation of the DataFrame before the chart can be created. See the comments in the code below.

Add the code to create a bar chart:

```python
from importlib import resources

import pandas as pd
import plotly.express as px


def bar_gender(event_type):
    """
    Creates a stacked bar chart showing change in the ration of male and female competitors in the summer and winter paralympics.

    Parameters
    event_type: str Winter or Summer

    Returns
    fig: Plotly Express bar chart
    """
    cols = ['type', 'year', 'host', 'participants_m', 'participants_f', 'participants']
    with resources.path("data", "paralympics.csv") as path:
        df_events = pd.read_csv(path, usecols=cols)
        # Drop Rome as there is no male/female data
        # Drop rows where male/female data is missing
        df_events = df_events.dropna(subset=['participants_m', 'participants_f'])
        df_events.reset_index(drop=True, inplace=True)

        # Add new columns that each contain the result of calculating the % of male and female participants
        df_events['Male'] = df_events['participants_m'] / df_events['participants']
        df_events['Female'] = df_events['participants_f'] / df_events['participants']

        # Sort the values by Type and Year
        df_events.sort_values(['type', 'year'], ascending=(True, True), inplace=True)
        # Create a new column that combines Location and Year to use as the x-axis
        df_events['xlabel'] = df_events['host'] + ' ' + df_events['year'].astype(str)

        # Create the stacked bar plot of the % for male and female
        df_events = df_events.loc[df_events['type'] == event_type]
        fig = px.bar(df_events,
                     x='xlabel',
                     y=['Male', 'Female'],
                     title=f'How has the ratio of female:male participants changed in {event_type} paralympics?',
                     labels={'xlabel': '', 'value': '', 'variable': ''},
                     template="simple_white"
                     )
        fig.update_xaxes(ticklen=0)
        fig.update_yaxes(tickformat=".0%")
        return fig
```

## Add the chart to the layout

In the Dash main app file, `paralympics_dash.py`, add code to create an instance of the bar chart and then add the
chart into the layout.

1. Create a variable that is the bar chart using the function you created in the last step.
2. Add a [Dash Core Components graph object](https://dash.plotly.com/dash-core-components/graph), `dcc.Graph()` to the
   layout. Use the `figure=` and `id=` attributes as you did for the line chart.

If not already running, run the Dash app and check that the chart displays.

## Add styling

Try and change some of the [styling options](https://plotly.com/python/styling-plotly-express/) of the bar chart e.g.
add a title, change the
colour of the bars (`color_discrete_map={'Male': 'blue', 'Female': 'green'}`).

[Next activity](2-4-scatter-map.md)