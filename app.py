from flask import Flask
from database.db import initialize_db
from flask_cors import CORS
from routes.images import images

app = Flask(__name__)
app.config.from_envvar("ENV_FILE_LOCATION")
CORS(app)

initialize_db(app)
app.register_blueprint(images)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
