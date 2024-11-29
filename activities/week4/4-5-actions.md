# Test that involve sequences of user actions

For this test:

- Find the id for the card and find the title element
- Find the map 
- Find a map marker and hover which should display a card.
- Find the card, the title should change.

[Selenium interaction functions](https://www.selenium.dev/documentation/webdriver/elements/interactions/) include
click(), send_keys(), submit() and clear().

These don't cover this case where we want to hover. Instead, use
the [Actions API](https://www.selenium.dev/documentation/webdriver/actions_api/).

```python
from selenium.webdriver import ActionChains


def test_map_marker_select_updates_card(dash_duo):
    """
    GIVEN the app is running which has a <div id='map>
    THEN there should not be any elements with a class of 'card' one the page
    WHEN a marker in the map is selected
    THEN there should be one more card on the page then there was at the start
    AND there should be a text value for the h6 heading in the card
    """
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)
    # Wait for the div with id of card to be on the page
    dash_duo.wait_for_element("#card", timeout=2)
    # There is no card so finding elements with a bootstrap class of 'card' should return 0
    cards = dash_duo.driver.find_elements(By.CLASS_NAME, "card")
    cards_count_start = len(cards)

    # Find the first map marker
    marker_selector = '#map > div.js-plotly-plot > div > div > svg:nth-child(1) > g.geolayer > g > g.layer.frontplot > g > g > path:nth-child(1)'
    marker = dash_duo.driver.find_element(By.CSS_SELECTOR, marker_selector)

    # Use the Actions API and build a chain to move to the marker and hover
    ActionChains(dash_duo.driver).move_to_element(marker).pause(1).perform()

    # Check there is now 1 card on the page
    cards_end = dash_duo.driver.find_elements(By.CLASS_NAME, "card")
    cards_count_end = len(cards_end)
    # There should be 1 more card
    assert cards_count_end - cards_count_start == 1

    # Wait for the element with class of 'card'
    dash_duo.wait_for_element(".card", timeout=1)
    # Find the h6 element of the card
    card = dash_duo.find_element("#card > div > div > h6")
    # The test should be Rome as it is the first point, though this assertion just checks the length of the text
    assert len(card.text) > 2
```

Run the test.

## Try it yourself

Run the Dash app so that you know what it contains.

Try to identify a few more tests you could write.

Write the tests and try running them.

## Other techniques

## Links

Dash have [tests for their code in GitHub](https://github.com/plotly/dash/tree/dev/tests). It can be useful
to see how they structure their own tests.

[Sean McCarthy's Dash testing tutorial](https://mccarthysean.dev/005-03-Dash-Testing). He uses the dash_thread_server
and dash_br fixtures rather than dash_duo, however it gives a number of examples of different ways to select elements on
the page for testing.

[Building unit tests for dash applications](https://plotly.com/blog/building-unit-tests-for-dash-applications/). This
goes beyond what is expected for the coursework and tests callbacks and uses mocks. Useful if you are already familiar
with testing and want to expand your knowledge.

[Plotly Dash Testing official documentation](https://dash.plotly.com/testing)

