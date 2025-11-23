import connexion

app = connexion.App(__name__, specification_dir='.')
app.add_api('openapi.yaml')

flask_app = app.app   # Access underlying Flask app

@flask_app.route("/")
def home():
    return "ML API running! Try /models/irisClassifier", 200

application = app.app
