# COMP0034 2025 Computer practicals

This repository contains the practicals for the COMP0034 module for the academic year 2024-25.

## Instructions for using this repository

1. Fork this repository to your own GitHub account.
2. Clone the forked repository to your local machine (e.g. in VS Code or PyCharm).
3. Each week, update the repository using the 'Sync fork' button in GitHub to check for changes, if it is out of date
   then select the 'Update branch' button.

## Activity instructions and code files

The `activities` folder contains the activity instructions for each week.

The code sub-packages packages with the `src` directory tree is not typical and is used so that students only need to
have one repository for all the tutorials. You would not usually have several different applications within a package.

The `src` directory contains three packages:

1. `code-samples`: snippets of code to illustrate concepts
2. `student`: use this package to make your changes when you complete the activities
3. `tutor`: this package is maintained by the course tutor and will be updated each week

Within these packages there are separate subpackages for each of the applications. `data` is duplicated in `student` and
`tutor`, allowing you to make changes to the student version if needed.

The sub-packages are:

- `dash-single`: use this for the Dash single page app activities in weeks 1-5
- `dash-multi`: use this for the optional Dash multi-page app activity in week 1
- `data`: the database and data files that you will need for the apps
- `flask-paralympics`: use this for the Flask activities in weeks 6-10

## Weekly activities

Please refer to the weekly folders in `activities`.

- Week 1 Basic Dash app with HTML layout and Bootstrap CSS
- Week 2 Adding charts to a Dash app with Plotly Express and Plotly Go
- Week 3 Adding interactivity to a Dash app using callbacks
- Week 4 Testing dash using Pytest with Selenium Webdriver
- Week 5 No mandatory content. This will be used for any additional activities or examples that might arise during weeks
  1 to 4.
- Week 6 Create and configure a Flask app
- Week 7 Model classes and database interaction with Flask-SQLAlchemy
- Week 8 Jinja templates and Bootstrap styling
- Week 9 Testing Flask routes
- Week 10 No mandatory content. This will be used for any additional activities or examples that might arise during
  weeks 6 to 9.
