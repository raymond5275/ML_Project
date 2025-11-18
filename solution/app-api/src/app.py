from connexion import FlaskApp


app = FlaskApp(__name__)
app.add_api('openapi.yaml')


application = app.app


if __name__ == '__main__':
    app.run(port=8080)