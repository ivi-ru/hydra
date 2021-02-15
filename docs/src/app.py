from flask import Flask, json

from api_spec import get_apispec
from power import blueprint_power
from swagger import swagger_ui_blueprint, SWAGGER_URL

app = Flask(__name__)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(blueprint_power)


@app.route('/swagger')
def create_swagger_spec():
    return json.dumps(get_apispec(app).to_dict())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
