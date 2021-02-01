from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields


DOCS_FILENAME = 'docs.yaml'


class InputSchema(Schema):
    number = fields.Int(description="Число", required=True, example=5)
    power = fields.Int(description="Степень", required=True, example=2)


class OutputSchema(Schema):
    result = fields.Int(description="Результат", required=True, example=25)


class ErrorSchema(Schema):
    error = fields.String(description="Сообщение об ошибке", required=True, example='Invalid input parameter number')


def get_apispec(app):
    """ Формируем объект APISpec.

    :param app: объект Flask приложения
    """
    spec = APISpec(
        title="My App",
        version="1.0.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    spec.components.schema("Input", schema=InputSchema)
    spec.components.schema("Output", schema=OutputSchema)
    spec.components.schema("Error", schema=ErrorSchema)

    create_tags(spec)

    load_docstrings(spec, app)

    write_yaml_file(spec)

    return spec


def create_tags(spec):
    """ Создаем теги.

    :param spec: объект APISpec для сохранения тегов
    """
    tags = [{'name': 'math', 'description': 'Математические функции'}]

    for tag in tags:
        print(f"Добавляем тэг: {tag['name']}")
        spec.tag(tag)


def load_docstrings(spec, app):
    """ Загружаем описание API.

   :param spec: объект APISpec, куда загружаем описание функций
   :param app: экземпляр Flask приложения, откуда берем описание функций
    """
    with app.test_request_context():
        for fn_name in app.view_functions:
            if fn_name == 'static':
                continue
            print(f"Загружаем описание функций: {fn_name}")
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)


def write_yaml_file(spec: APISpec):
    """ Экспортируем объект APISpec в YAML файл.

    :param spec: объект APISpec
    """
    with open(DOCS_FILENAME, 'w') as file:
        file.write(spec.to_yaml())
    print(f'Сохранили документацию в {DOCS_FILENAME}')
