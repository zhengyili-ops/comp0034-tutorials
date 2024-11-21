# Implement the checkbox callback for the gender bar chart

## Callback behaviour

### Easier version:

When one or both checkboxes are selected, the callback should display the selected chart(s). This may be summer or
winter.

### More challenging version:

When one or both checkboxes are selected, the callback should display the selected chart(s). This may be summer, winter
or both.

Currently, the app has one bar chart component in the layout. Your function will need to be able to add one or two
charts. You will need to work out the logic for this, options might include:

- Change the layout so that the bar charts go in a html.Div which becomes the Output. The callback then creates a
  dcc.Chart component for each of the items in the list, and adds these as 'children=' to the Div.
- Add summer and winter chart components the layout and make these hidden/shown based on the checkbox selection. CSS
  properties can be used to show and hide elements.

## Code logic

Use the logic given for the dropdown in the last activity to work out the code for this yourself.

1. Find the `id` of the checkbox component and the name of the parameter that holds the selected value. A checkbox takes
   multiple values so it returns a list `[]` that can have one or two values e.g. `['summer']`, `['summer', 'winter']`.
   This list is the `component_property`.
2. Find the `id` of the bar chart component; the name of the parameter to update is the `figure`
3. The function should create a bar chart figure using the `figures/create_bar_chart(event_type)` function created last
   week (you may have used a different name for the function). This function takes a string as its parameter.
4. Write the callback function.

    - Easier version: The callback takes the first value only from the list and creates a single bar chart and returns
      this figure.
    - Challenging version: The callback will need to take the list and create a bar chart for each entry in the list.
      The results need to be output to the layout. See the notes on the behaviour above for suggestions as to how you
      might approach this.

Remember the general structure of a callback is:

```python
# The callback decorator
@callback(
    # The Output(s)
    Output(component_id='my-output', component_property='children'),
    # The Input(s)
    Input(component_id='my-input', component_property='value')
)
# The function that will make the changes. 
# It takes the value captured from the Input property as the `input_value`. Give this a meaningful name.
# It returns whatever change you want to make in the function. In this example it returns a string with the input value.
def update_output_div(input_value):
    return f'Output: {input_value}'
```

[Next activity](3-4-map-card-callback.md)