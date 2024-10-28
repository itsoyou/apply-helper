import os

from flask import Flask

from apply_helper.config import Config, logger
from apply_helper.routes import init_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_routes(app)
    return app


if __name__ == "__main__":

    from apply_helper.assistant import create_assistant

    app = create_app()
    absolute_path = os.path.abspath(Config.UPLOAD_FOLDER)
    if not os.path.exists(absolute_path):
        logger.debug("New directory created: %s", absolute_path)
        try:
            os.makedirs(absolute_path, exist_ok=True)
        except PermissionError:
            logger.error(
                "Error: No permission to create directory at %s", absolute_path
            )
            raise
        except Exception as e:
            logger.error(
                "Error creating directory %s, %s", absolute_path, str(e)
            )
            raise
    Config.ASSISTANT_ID = create_assistant()
    app.run(debug=True)
