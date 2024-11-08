# Import the Dash framework
from dash import Dash, html

# Create a new Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.Div(children='Hello World')
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    # Runs on port 8050 by default. If you have a port conflict, add the parameter port=   e.g. port=8051
