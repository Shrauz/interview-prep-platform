from flask import Flask,jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # db.init_app(app)
    # api.init_app(app)
    app.app_context().push()
    return app

app = create_app()

@app.route("/")
def index():
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True)