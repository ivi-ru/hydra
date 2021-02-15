from flask import Blueprint, current_app, json, request

blueprint_power = Blueprint(name="power", import_name=__name__)


@blueprint_power.route('/power')
def power():
    """
    ---
    get:
      summary: Возводит число в степень
      parameters:
        - in: query
          schema: InputSchema
      responses:
        '200':
          description: Результат возведения в степень
          content:
            application/json:
              schema: OutputSchema
        '400':
          description: Не передан обязательный параметр
          content:
            application/json:
              schema: ErrorSchema
      tags:
        - math
    """
    args = request.args

    number = args.get('number')
    if number is None:
        return current_app.response_class(
            response=json.dumps(
                {'error': 'Invalid input parameter number'}
            ),
            status=400,
            mimetype='application/json'
        )

    power = args.get('power')
    if power is None:
        return current_app.response_class(
            response=json.dumps(
                {'error': 'Invalid input parameter power'}
            ),
            status=400,
            mimetype='application/json'
        )

    return current_app.response_class(
        response=json.dumps(
            {'response': int(number)**int(power)}
        ),
        status=200,
        mimetype='application/json'
    )
