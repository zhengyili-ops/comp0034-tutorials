# Other examples

The following sign posts resources for features not covered in this tutorial.

## Integrating your Dash app in your Flask app

Try [Integrate Dash Apps into Your Flask App](https://ploomber.io/blog/dash-in-flask/), though ignore the part about
deploying to the cloud as you are not allowed to do that for the courswork.

There is a Hackers and Slackers tutorial on integrating Flask and Dash however both apps have changed substantially
since this was written.

## Authentication

Please do not apply authentication in your coursework unless it is fundamental to how your app works, for example if you
need to know an identity to be able to complete features such as customising data and saving those customisations.
It is very widely documented with readily available boilerplate code, and so is not likely to improve the marks awarded
for your app.

A few tutorial links that cover authentication:

- [Miguel Grinberg's mega tutorial episode on login](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins)
- [Flask Friday - YouTube](https://www.youtube.com/watch?v=bxyaJ8w_wak)
- [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login)

## REST API

REST APIs have not been covered in the module this year.

If you wish to attempt this you need to understand what a REST API is, as well as how to construct one.

REST APIs return structured data, typically JSON, and do not have HTML pages. They are used by developers to access data
that they can use in their own apps. You get the data from a REST API using an HTTP request.

If you decide to generate this type of app in the coursework:

- include code that can be used with [HTTPie terminal](https://httpie.io/cli) to check each route. Required for marking.
- if you implement authentication, provide credentials the marker can use. Required for marking.

You will not be generating pages so please make sure that your app evidences sufficient 'features', consider:

- use SQLAlchemy to interact with the database instead of sqlite3
- document with swagger or other

### REST API links

#### What is a REST API?

- [Postman: what is a REST API?](https://blog.postman.com/rest-api-examples/)
- [AWS: What is RESTful API?](https://aws.amazon.com/what-is/restful-api/)
- [Freecodecamp: How to use REST API](https://www.freecodecamp.org/news/how-to-use-rest-api/) - misleading title,
  explains what a REST api is.

#### Tools

- [Swagger](https://swagger.io/docs/specification/v2_0/what-is-swagger/)
- [Postman](https://www.postman.com/downloads/)
- [HTTPie terminal](https://httpie.io/cli)

#### Developing a REST API in Flask

- [Analytics Vidhya: Rest API | Complete Guide on Rest API with Python and Flask](https://www.analyticsvidhya.com/blog/2022/01/rest-api-with-python-and-flask/) -
  you may need to subscribe to this, if so use one of the other links
- [Real Python: Python REST APIs With Flask, Connexion, and SQLAlchemy](https://realpython.com/flask-connexion-rest-api/) -
  also generates swagger documentation
- [Miguel Grinberg: The Flask Mega-Tutorial, Part XXIII: Application Programming Interfaces (APIs) ](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis) -
  uses FlaskSQLAlechemy and implements authentication
- [Python Basics](https://pythonbasics.org/flask-rest-api/) - does not require a 3rd party library